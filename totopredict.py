import random
import urllib3
import certifi 
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import csv
 
# # WEBスクレイピング処理（公式HPから指定回の情報を取得） 
# def get_toto(kuzi_num):
#     # URL指定＋指定回
#     url = "https://store.toto-dream.com/dcs/subos/screen/pi01/spin000/PGSPIN00001DisptotoLotInfo.form?holdCntId=" + kuzi_num
#     http = urllib3.PoolManager()
 
#     try:
#         r = http.request('GET', url)
#         # ページ全体取得
#         soup = BeautifulSoup(r.data,'html.parser')
#     except:
#         print("ページをGETできませんでした。")
#         sys.exit(1)
 
#     # テーブル情報取得
#     table_soup = soup.findAll("table",{"class":"kobetsu-format3"})[0]
#     # 行情報取得
#     table_tr = table_soup.findAll("tr")
 
#     rows = []
#     # 行数分繰り返し
#     for row in table_tr:
#         cols = []
#         # セル分繰り返し
#         for cell in row.findAll(['td','th']):
#             # カラム情報を１個ずつ追加していく
#            cols.append(cell.get_text().strip())
#         rows.append(cols)
 


#     return rows 
 

# #勝ち負けを判定する関数(Win Draw Loose)
# def get_wdl(game_list,total_mach_list):
     
#     # wdl_homeaway = random.choices([0,1,2], weights=[ha_w,ha_d,ha_l])
#     # wdl_random = random.choices([0,1,2])
#     # wdl_select = random.choices([wdl_homeaway[0],wdl_random[0]], weights=[ha,rd])

#     # 予想表示リスト
#     wdl_list =['X - -','- X -','- - X']

#     home_team = game_list.pop(4)
#     away_team = game_list.pop(5)

#     for row in total_mach_list:
#         if home_team == row[2]:
#             print(home_team)
#             print(row[2])
#             break





#     # print("勝敗データ")
#     # print(total_mach_list)




 
#     return wdl_list[0]

# WEBスクレイピング処理（投票結果取得）
def get_mach_info(kuzi_num,setu):

    # URL指定(TOTOサイト)
    url = "https://store.toto-dream.com/dcs/subos/screen/pi09/spin003/PGSPIN00301InitVoteRate.form?holdCntId=" + kuzi_num +"&commodityId=01" 
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
            cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7] = cols[4], cols[5], cols[6],'','', cols[3], cols[7], ''

            for num in range(3):
                index = cols[num].find('（') +1
                index2 = cols[num].find('）') -1
                cols[num] = float(cols[num][index:index2])/100

            rows.append(cols)


    # URL指定(jリーグサイト)
    url2 = "https://data.j-league.or.jp/SFRT01/?search=search&yearId=2021&yearIdLabel=2021年&competitionId=492&competitionIdLabel=明治安田生命Ｊ１リーグ&competitionSectionId=" + setu +"&competitionSectionIdLabel=第" + setu + "節&search=search"
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url2)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    # テーブル情報取得
    table_soup2 = soup.findAll("table",{"class":"standings-table00"})[0]
    # 行情報取得
    table_tr2 = table_soup2.findAll("tr")

    rows2 = []
    # 行数分繰り返し
    cnt=0
    for row2 in table_tr2:
        cols2 = []
        # セル分繰り返し
        for cell2 in row2.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
            cols2.append(cell2.get_text().strip())
        rows2.append(cols2)
    


    # ランキング取得
    for ritem in rows:
        print(ritem[5])
        print(ritem[6])
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

        print(ritem[5])
        print(ritem[6])


        for ritem2 in rows2:
            # ホームランキング
            if ritem[5] in ritem2[2]:
                ritem[3] = ritem2[1]
            # アウェイランキング
            if ritem[6] in ritem2[2]:
                ritem[4] = ritem2[1]

    print(rows)
    # rows2



    f = open('out.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['homeper', 'drawper', 'awayper', 'homerank', 'aweyrank', 'hometeam', 'aweyteam', 'homegoal', 'aweygoal'])
    writer.writerows(rows)
    f.close()




    return rows 


# 0_メイン処理 
def main():
    #引数の処理、lenが3(引数は一つ)であれば処理継続
    args = sys.argv
    if len(args) == 4:
        # WEBスクレイピング
        # 分析情報を収集する
        get_mach_info(args[1],args[2])



        # # 1：TOTAL勝敗
        # total_mach_list = get_mach_info(args[2],"3")
        # # 2：ホームでの勝敗
        # home_mach_list = get_mach_info(args[2],"1")
        # # 3：ホーム/アウェイでの勝敗
        # away_mach_list = get_mach_info(args[2],"2")
        # # away_mach_list.pop(0)

        # 学習
        train = pd.read_csv('out3.csv')
        train.head




        # # WEBスクレイピング（公式HPから指定回の対戦情報を取得）
        # game_list = get_toto(args[1])
    else:
        # 引数取得エラー（開催回の取得エラー）
        print("開催回を入れて下さい。")
        sys.exit(1)
 
    # #テーブル処理:ヘッダ
    # tbl_head = ["試合","開催日","時間","競技場","ホーム","VS","アウェイ","勝敗"]
    # #テーブル処理:項目
    # del game_list[0]
 
    # wdl_dict ={
    #     'ha_w':4,
    #     'ha_d':1,
    #     'ha_l':2,
    #     'ha':2,
    #     'rd':1
    # }

 
    # #勝敗を予測し列に追加 
    # for i in range(len(game_list)):
    #     game_list[i].append(get_wdl(game_list[i],total_mach_list))

    # print(tabulate(game_list,tbl_head,tablefmt="grid"))
 
if __name__ == '__main__':
    main()