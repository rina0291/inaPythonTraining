import random
import urllib3
import certifi 
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate

 
# WEBスクレイピング処理（公式HPから指定回の情報を取得） 
def get_toto(kuzi_num):
    # URL指定＋指定回
    url = "https://store.toto-dream.com/dcs/subos/screen/pi01/spin000/PGSPIN00001DisptotoLotInfo.form?holdCntId=" + kuzi_num
    http = urllib3.PoolManager()
 
    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)
 
    # テーブル情報取得
    table_soup = soup.findAll("table",{"class":"kobetsu-format3"})[0]
    # 行情報取得
    table_tr = table_soup.findAll("tr")
 
    rows = []
    # 行数分繰り返し
    for row in table_tr:
        cols = []
        # セル分繰り返し
        for cell in row.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
           cols.append(cell.get_text().strip())
        rows.append(cols)
 
    return rows 
 

#勝ち負けを判定する関数(Win Draw Loose)
def get_wdl(game_list,total_mach_list):
     
    # wdl_homeaway = random.choices([0,1,2], weights=[ha_w,ha_d,ha_l])
    # wdl_random = random.choices([0,1,2])
    # wdl_select = random.choices([wdl_homeaway[0],wdl_random[0]], weights=[ha,rd])

    # 予想表示リスト
    wdl_list =['X - -','- X -','- - X']

    home_team = game_list.pop(4)
    away_team = game_list.pop(5)

    for row in total_mach_list:
        if home_team == row[2]:
            print(home_team)
            print(row[2])
            break





    # print("勝敗データ")
    # print(total_mach_list)




 
    return wdl_list[0]

# WEBスクレイピング処理（TOTAL勝敗取得）
def get_mach_info(kuzi_num,mach_flg):
    # URL指定
    url = "https://data.j-league.or.jp/SFRT01/?search=search&yearId=2021&yearIdLabel=2021年&competitionId=492&competitionIdLabel=明治安田生命Ｊ１リーグ&competitionSectionId=" + kuzi_num +"&competitionSectionIdLabel=第" + kuzi_num + "節&homeAwayFlg=" + mach_flg
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

    rows = []
    # 行数分繰り返し
    for row in table_tr:
        cols = []
        # セル分繰り返し
        for cell in row.findAll(['td','th']):
            # カラム情報を１個ずつ追加していく
           cols.append(cell.get_text().strip())
        rows.append(cols)

    return rows 


# メイン処理 
def main():
    #引数の処理、lenが3(引数は一つ)であれば処理継続
    args = sys.argv
    if len(args) == 3:
        # WEBスクレイピング
        # 分析情報を収集する
        # 1：TOTAL勝敗
        total_mach_list = get_mach_info(args[2],"3")
        total_mach_list.pop(0)
        # 2：ホームでの勝敗
        home_mach_list = get_mach_info(args[2],"1")
        home_mach_list.pop(0)
        # 2：ホーム/アウェイでの勝敗
        away_mach_list = get_mach_info(args[2],"2")
        away_mach_list.pop(0)

        # 3：直近の勝敗



        # 4：戦績表
        











        # WEBスクレイピング（公式HPから指定回の対戦情報を取得）
        game_list = get_toto(args[1])
    else:
        # 引数取得エラー（開催回の取得エラー）
        print("開催回を入れて下さい。")
        sys.exit(1)
 
    #テーブル処理:ヘッダ
    tbl_head = ["試合","開催日","時間","競技場","ホーム","VS","アウェイ","勝敗"]
    #テーブル処理:項目
    del game_list[0]
 
    # wdl_dict ={
    #     'ha_w':4,
    #     'ha_d':1,
    #     'ha_l':2,
    #     'ha':2,
    #     'rd':1
    # }

 
    #勝敗を予測し列に追加 
    for i in range(len(game_list)):
        game_list[i].append(get_wdl(game_list[i],total_mach_list))

    print(tabulate(game_list,tbl_head,tablefmt="grid"))
 
if __name__ == '__main__':
    main()