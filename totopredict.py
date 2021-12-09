import random
import urllib3
import certifi 
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import csv
from sklearn import tree

# WEBスクレイピング処理1（TOTOサイトから投票結果取得）
def get_toto_info(totoId):
    # URL指定(TOTOサイト)
    url = "https://store.toto-dream.com/dcs/subos/screen/pi09/spin003/PGSPIN00301InitVoteRate.form?holdCntId=" + totoId +"&commodityId=01" 
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"kobetsu-format2 mb10"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")

    rows = []
    # 行数分繰り返し
    cnt=0
    for row in table_tr:
        cnt += 1
        if cnt % 3 == 0:
            cols = []
            # セル分繰り返し
            for cell in row.findAll(['td','th']):
                # カラム情報を１個ずつ追加していく
                cols.append(cell.get_text().strip())
            # 学習CSV用に順序入れ替え
            cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7] = cols[4], cols[5], cols[6],'','', cols[3], cols[7], ''

            # 投票率編集
            for num in range(3):
                index = cols[num].find('（') +1
                index2 = cols[num].find('）') -1
                cols[num] = float(cols[num][index:index2])/100
            
            cols.append('')
            rows.append(cols)
    # 返却
    return rows

# WEBスクレイピング処理2（J1リーグサイトから指定節順位を取得）
def get_j1rank_info(rows,setu):
    # URL指定(j1リーグサイト)
    url = "https://data.j-league.or.jp/SFRT01/?search=search&yearId=2021&yearIdLabel=2021年&competitionId=492&competitionIdLabel=明治安田生命Ｊ１リーグ&competitionSectionId=" + setu +"&competitionSectionIdLabel=第" + setu + "節&search=search"
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"standings-table00"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")

    rows2 = []
    # 行数分繰り返し
    cnt=0
    for row2 in table_tr:
        cols2 = []
        # セル分繰り返し
        for cell2 in row2.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
            cols2.append(cell2.get_text().strip())
        rows2.append(cols2)
    
    # ランキングを取得して学習CSV用に追加
    for ritem in rows:
        ritem[5] = ritem[5].replace('Ｃ大阪','セレッソ大阪')
        ritem[5] = ritem[5].replace('横浜Ｍ','横浜Ｆ・マリノス')
        ritem[5] = ritem[5].replace('Ｆ東京','ＦＣ東京')
        ritem[5] = ritem[5].replace('Ｇ大阪','ガンバ大阪')
        ritem[5] = ritem[5].replace('横浜Ｃ','横浜ＦＣ')

        ritem[6] = ritem[6].replace('Ｃ大阪','セレッソ大阪')
        ritem[6] = ritem[6].replace('横浜Ｍ','横浜Ｆ・マリノス')
        ritem[6] = ritem[6].replace('Ｆ東京','ＦＣ東京')
        ritem[6] = ritem[6].replace('Ｇ大阪','ガンバ大阪')
        ritem[6] = ritem[6].replace('横浜Ｃ','横浜ＦＣ')

        for ritem2 in rows2:
            # ホームランキング
            if ritem[5] in ritem2[2]:
                ritem[3] = ritem2[1]
            # アウェイランキング
            if ritem[6] in ritem2[2]:
                ritem[4] = ritem2[1]
    # 返却
    return rows

# WEBスクレイピング処理3（J2リーグサイトから指定節順位を取得）
def get_j2rank_info(rows,setu):
    # URL指定(J2リーグサイト)
    url = "https://data.j-league.or.jp/SFRT01/?competitionSectionIdLabel=第" + setu + "節&competitionIdLabel=明治安田生命Ｊ２リーグ&yearIdLabel=2021年&yearId=2021&competitionId=493&competitionSectionId=40&search=search"
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"standings-table00"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")

    rows2 = []
    # 行数分繰り返し
    cnt=0
    for row2 in table_tr:
        cols2 = []
        # セル分繰り返し
        for cell2 in row2.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
            cols2.append(cell2.get_text().strip())
        rows2.append(cols2)
    
    # ランキング取得
    for ritem in rows:
        ritem[5] = ritem[5].replace('東京Ｖ','東京ヴェルディ')
        ritem[6] = ritem[6].replace('東京Ｖ','東京ヴェルディ')
        for ritem2 in rows2:
            # ホームランキング
            if ritem[5] in ritem2[2]:
                ritem[3] = ritem2[1]
            # アウェイランキング
            if ritem[6] in ritem2[2]:
                ritem[4] = ritem2[1]
    # 返却
    return rows

# WEBスクレイピング処理4（J3リーグサイトから指定節順位を取得）
def get_j3rank_info(rows,setu):
    # URL指定(J2リーグサイト)
    url = "https://data.j-league.or.jp/SFRT01/?competitionSectionIdLabel=第" + setu + "節&competitionIdLabel=明治安田生命Ｊ3リーグ&yearIdLabel=2021年&yearId=2021&competitionId=494&competitionSectionId=27&search=search"
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"standings-table00"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")

    rows2 = []
    # 行数分繰り返し
    cnt=0
    for row2 in table_tr:
        cols2 = []
        # セル分繰り返し
        for cell2 in row2.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
            cols2.append(cell2.get_text().strip())
        rows2.append(cols2)
    
    # ランキング取得
    for ritem in rows:
        ritem[5] = ritem[5].replace('Ｙ横浜','Ｙ．Ｓ．Ｃ．Ｃ．横浜')
        ritem[6] = ritem[6].replace('Ｙ横浜','Ｙ．Ｓ．Ｃ．Ｃ．横浜')

        for ritem2 in rows2:
            # ホームランキング
            if ritem[5] in ritem2[2]:
                ritem[3] = ritem2[1]
            # アウェイランキング
            if ritem[6] in ritem2[2]:
                ritem[4] = ritem2[1]
    # 返却
    return rows

# WEBスクレイピング処理5（TOTOサイトから試合結果ゴール数取得）
def get_totogoal_info(rows,totoId):
    # URL指定(totoサイト結果)
    url = "https://store.toto-dream.com/dcs/subos/screen/pi04/spin011/PGSPIN01101LnkHoldCntLotResultLsttoto.form?holdCntId=" + totoId
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"kobetsu-format2 mb10"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")

    rows2 = []
    # 行数分繰り返し
    cnt=0
    for row2 in table_tr:
        cols2 = []
        # セル分繰り返し
        for cell2 in row2.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
            cols2.append(cell2.get_text().strip())
        rows2.append(cols2)
    
    rows2.pop(0)
    rows2.pop(0)
    
    cnt=0
    for item in rows2:
        if item[4]=="中止":
            rows[cnt][7] = 0
            rows[cnt][8] = 0    
        else:
            goal = item[4].split('-')
            rows[cnt][7] = goal[0]
            rows[cnt][8] = goal[1]
        cnt += 1

    # 返却
    return rows

# CSV出力
def write_csv_data(rows,cnt,mode):
    if mode == "t":
        # 学習データ
        f = open('out.csv', 'a', newline='')
    else:
        # 予想データ
        f = open('yosou.csv', 'w', newline='')

    writer = csv.writer(f)
    # 初回以外はヘッダー削除
    if mode == "t":
        if cnt == 0:
            # 学習データ
            writer.writerow(['homeper', 'drawper', 'awayper', 'homerank', 'aweyrank', 'hometeam', 'aweyteam', 'homegoal', 'aweygoal'])
    else:
        # 予想データ
        writer.writerow(['homeper', 'drawper', 'awayper', 'homerank', 'aweyrank', 'hometeam', 'aweyteam'])
        for row in rows:
            if len(row) == 10:
                row.pop(9)
            row.pop(8)
            row.pop(7)

    writer.writerows(rows)
    f.close()


# 0_メイン処理 
def main():
    #引数の処理、引数が正しければ処理継続
    args = sys.argv
    if len(args) == 3:
        # CSVクリア
        with open("out.csv", 'r+') as f:
            f.truncate(0)

        cnt = 0
        toto = int(args[1]) - int(args[2])
        j1setu = toto - 1232
        j2setu = toto - 1228
        j3setu = toto - 1240

        # スクレイピング処理纏め
        for i in range(int(args[2])):
            # 特定回はSKIP
            if toto+cnt == 1250:
                cnt +=1
                continue         

            print("第"+str(toto+cnt)+"回処理中")
            # WEBスクレイピング処理1（TOTOサイトから投票結果取得）
            info_rows = get_toto_info(str(toto+cnt))

            # WEBスクレイピング処理2（J1リーグサイトから指定節順位を取得）
            info_rows = get_j1rank_info(info_rows,str(j1setu+cnt))
            print("J1："+str(j1setu+cnt)+"節")

            # WEBスクレイピング処理3（J2リーグサイトから指定節順位を取得）
            info_rows = get_j2rank_info(info_rows,str(j2setu+cnt))
            print("J2："+str(j2setu+cnt)+"節")

            # WEBスクレイピング処理4（J3リーグサイトから指定節順位を取得）
            info_rows = get_j3rank_info(info_rows,str(j3setu+cnt))
            print("J3："+str(j3setu+cnt)+"節")

            # WEBスクレイピング処理5（TOTOサイトから試合結果ゴール数取得）
            info_rows = get_totogoal_info(info_rows,str(toto+cnt))

            # CSV出力
            write_csv_data(info_rows,cnt,"t")
            cnt +=1

        # # 予想CSV作成
        print("【予想CSV作成中】")
        sitei_toto = args[1]
        sitei_j1 = str(int(sitei_toto) - 1232) 
        sitei_j2 = str(int(sitei_toto) - 1228) 
        sitei_j3 = str(int(sitei_toto) - 1240) 


        # # WEBスクレイピング処理1（TOTOサイトから投票結果取得）
        info_rows = get_toto_info(sitei_toto)
        print("第"+sitei_toto+"回処理中")
        # # WEBスクレイピング処理2（J1リーグサイトから指定節順位を取得）
        info_rows = get_j1rank_info(info_rows,sitei_j1)
        print("J1；"+sitei_j1+"節")
        # # WEBスクレイピング処理3（J2リーグサイトから指定節順位を取得）
        info_rows = get_j2rank_info(info_rows,sitei_j2)
        print("J2；"+sitei_j2+"節")
        # # WEBスクレイピング処理4（J3リーグサイトから指定節順位を取得）
        info_rows = get_j3rank_info(info_rows,sitei_j3)
        print("J3；"+sitei_j3+"節")
        # CSV出力
        write_csv_data(info_rows,0,"e")

        # CSV読み込み
        train = pd.read_csv("out.csv",encoding='Shift_JIS')
        test =  pd.read_csv("yosou.csv",encoding='Shift_JIS')

        # 学習
        print("【学習開始】")
        print("【第" + args[1] +"回予想結果】");

        for i in range(2):
            if i == 0:
                #目的変数と説明変数を決定して取得
                target  = train['homegoal'].values #目的
            else:
                target  = train['aweygoal'].values #目的
                
    
            explain = train[['homeper','drawper','awayper','homerank','aweyrank']].values #説明
            #決定木の作成
            d_tree = tree.DecisionTreeClassifier()
            #fit()で学習させる。第一引数に説明変数、第二引数に目的変数
            d_tree = d_tree.fit(explain, target)
            # 予想
            if i == 0:
                print("【ホームチームゴール数予想】")
            else:
                print("【アウェイチームゴール数予想】")
            #testデータから説明変数を抽出
            test_explain = test[['homeper','drawper','awayper','homerank','aweyrank']].values
            #predict()メソッドで予測する
            prediction = d_tree.predict(test_explain)

            #出力結果を確認する
            #予測データの中身
            print(prediction)



    else:
        # 引数取得エラー（開催回の取得エラー）
        print("引数の数が誤っています")
        sys.exit(1)
 
 
if __name__ == '__main__':
    main()