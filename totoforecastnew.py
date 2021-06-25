import random
import urllib3
import certifi 
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate

 
# WEBスクレイピング処理（公式HPから指定回の情報を取得） 
def toto(kuzi_num):
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
 
def wdl(ha_w,ha_d,ha_l,ha,rd):
#勝ち負けを判定する関数(Win Draw Loose)
 
    wdl_list =['X - -','- X -','- - X']
     
    wdl_homeaway = random.choices([0,1,2], weights=[ha_w,ha_d,ha_l])
    wdl_random = random.choices([0,1,2])
 
    wdl_select = random.choices([wdl_homeaway[0],wdl_random[0]], weights=[ha,rd])
 
    return wdl_list[wdl_select[0]]

# 過去の情報を取得して返却
def getPastInformation(kuzi_num):
    # URL1指定
    url = "https://store.toto-dream.com/dcs/subos/screen/pi04/spin011/PGSPIN01101LnkHoldCntLotResultLsttoto.form?holdCntId=" + str(int(kuzi_num) - 1)
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url)
        # ページ全体取得
        soup = BeautifulSoup(r.data,'html.parser')
    except:
        print("ページをGETできませんでした。")
        sys.exit(1)

    return ""



# メイン処理 
def main():
    #引数の処理、lenが2(引数は一つ)であれば処理継続
    args = sys.argv
    if len(args) == 2:
        # WEBスクレイピング（過去の開催回情報を取得）
        getPastInformation(args[1])





        # WEBスクレイピング（公式HPから指定回の対戦情報を取得）
        game_list = toto(args[1])
    else:
        # 引数取得エラー（開催回の取得エラー）
        print("開催回を入れて下さい。")
        sys.exit(1)
 
    #テーブル処理:ヘッダ
    tbl_head = ["試合","開催日","時間","競技場","ホーム","VS","アウェイ","勝敗"]
    #テーブル処理:項目
    del game_list[0]
 
    wdl_dict ={
        'ha_w':4,
        'ha_d':1,
        'ha_l':2,
        'ha':2,
        'rd':1
    }
 
    #勝敗を予測し列に追加 
    for i in range(len(game_list)):
        game_list[i].pop()
        game_list[i].append(wdl(**wdl_dict))
 
    print(tabulate(game_list,tbl_head,tablefmt="grid"))
 
if __name__ == '__main__':
    main()