import random
from typing import Text
import urllib3
import certifi 
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import csv
from sklearn import tree

# WEBスクレイピング処理（TOTOサイトから投票結果取得）
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

    rows = []
    pageText = soup.find_all("p")
    if len(pageText) != 0:
        if 'ご指定の投票状況は表示できません' in soup.p.text:
            print("この回はTOTO未開催のためSKIP")
            return rows
        

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"kobetsu-format2 mb10"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")

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
            cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6] = cols[4], cols[5], cols[6], cols[3], cols[7], '',''
            cols.pop(7)

            # 投票率編集
            for num in range(3):
                index = cols[num].find('（') +1
                index2 = cols[num].find('）') -1
                cols[num] = float(cols[num][index:index2])/100
            
            rows.append(cols)
    # 返却
    return rows

# WEBスクレイピング処理（TOTOサイトから試合結果ゴール数取得）
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
            rows[cnt][5] = 0
            rows[cnt][6] = 0    
        else:
            goal = item[4].split('-')
            rows[cnt][5] = goal[0]
            rows[cnt][6] = goal[1]
        cnt += 1

    # 返却
    return rows

# CSV出力
def write_csv_data(rows,cnt,mode):
    if mode == "t":
        # 学習データ
        f = open('newOutput.csv', 'a', newline='')
    else:
        # 予想データ
        f = open('yosou.csv', 'w', newline='')

    writer = csv.writer(f)
    # 初回以外はヘッダー削除
    if mode == "t":
        if cnt == 0:
            # 学習データ
            writer.writerow(['homeper', 'drawper', 'awayper', 'hometeam', 'aweyteam', 'homegoal', 'aweygoal'])
    else:
        # 予想データ
        writer.writerow(['homeper', 'drawper', 'awayper', 'hometeam', 'aweyteam'])
        for row in rows:
            if len(row) == 8:
                row.pop(7)
            row.pop(6)
            row.pop(5)

    writer.writerows(rows)
    f.close()

# WEBスクレイピング処理（TOTOサイトから過去の開催回取得）
def get_past_toto():
    # URL指定(TOTOサイト)
    url = "https://store.toto-dream.com/dcs/subos/screen/pi04/spin011/PGSPIN01101LnkSeasonLotResultLsttoto.form?meetingFiscalYear=2022" 
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"kobetsu-format2 mb25"})[0]
    links = [url.get('href') for url in table_soup.find_all('a')]
    toto_no_info = []
    for link in links:
        toto_no_info.append(int(link[-4:]))
        
    return toto_no_info

# 0_メイン処理 
def main():
    # CSVクリア
    with open("newOutput.csv", 'a') as f:
        f.truncate(0)

    # toto今年度全開催回数を取得する
    toto_no_info = get_past_toto()
    # ★特殊処理（次回TOTOがないため）
    # toto_no_info.pop(0)

    cnt=0
    print("【学習用CSV作成中】")

    # スクレイピング処理纏め
    for no in toto_no_info:
        print("第"+str(no)+"回処理中")
        # WEBスクレイピング処理1（TOTOサイトから投票結果取得）
        info_rows = get_toto_info(str(no))
        if len(info_rows) == 0:
            continue
            
        # WEBスクレイピング処理5（TOTOサイトから試合結果ゴール数取得）
        info_rows = get_totogoal_info(info_rows,str(no))

        # CSV出力
        write_csv_data(info_rows,cnt,"t")
        cnt +=1

    # # 予想CSV作成
    print("【予想CSV作成中】")

    # # WEBスクレイピング処理1（TOTOサイトから投票結果取得）
    yosou_no = toto_no_info[0]+1
    info_rows = get_toto_info(str(yosou_no))
    print("第"+str(yosou_no)+"回処理中")
    # CSV出力
    write_csv_data(info_rows,0,"e")

    # CSV読み込み
    train = pd.read_csv("newOutput.csv",encoding='Shift_JIS')
    test =  pd.read_csv("yosou.csv",encoding='Shift_JIS')

    # 学習
    print("【学習開始】")
    print("【第" + str(yosou_no) +"回予想結果】");

    for i in range(2):
        if i == 0:
            #目的変数と説明変数を決定して取得
            target  = train['homegoal'].values #目的
        else:
            target  = train['aweygoal'].values #目的
            

        explain = train[['homeper','drawper','awayper']].values #説明
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
        test_explain = test[['homeper','drawper','awayper']].values
        #predict()メソッドで予測する
        prediction = d_tree.predict(test_explain)

        #出力結果を確認する
        #予測データの中身
        print(prediction)

 
if __name__ == '__main__':
    main()