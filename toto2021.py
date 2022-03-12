import random
from typing import Text
import certifi 
from tabulate import tabulate
import csvProcess
import scrapingProcess
import learningProcess

# 0_メイン処理 
def main():
    # CSVクリア
    csvProcess.csv_clear()

    # 学習用データ取得年度（TOTO開催年度）
    totoList = []
    totoList += ["2022","2021","2020","2019"]

    # toto年度別全開催回数を取得する
    toto_no_info = []
    for idx,totoYear in enumerate(totoList):
        if idx==0:
            toto_no_info = scrapingProcess.get_past_toto(totoYear)
        else:
            toto_no_info = toto_no_info + scrapingProcess.get_past_toto(totoYear)

    cnt=0

    # ＊＊最新回除外＊＊
    toto_no_info.pop(0)



    # 学習用CSV作成処理
    print("【学習用CSV作成中】")
    for no in toto_no_info:
        print("第"+str(no)+"回処理中")

        if no == 1163 or no == 1160:
            continue

        # WEBスクレイピング処理1（TOTOサイトから投票結果取得）
        info_rows = scrapingProcess.get_toto_info(str(no))
        if len(info_rows) == 0:
            continue
            
        # WEBスクレイピング処理2（TOTOサイトから試合結果ゴール数取得）
        info_rows = scrapingProcess.get_totogoal_info(info_rows,str(no))

        # CSV出力
        csvProcess.write_csv_data(info_rows,cnt,"t")
        cnt +=1

    # 予想回用CSV作成処理
    print("【予想CSV作成中】")

    # # WEBスクレイピング処理1（TOTOサイトから投票結果取得）
    yosou_no = toto_no_info[0]+1
    info_rows = scrapingProcess.get_toto_info(str(yosou_no))
    # CSV出力
    csvProcess.write_csv_data(info_rows,0,"e")


    # 学習処理
    print("【学習開始】")
    print("【第" + str(yosou_no) +"回予想結果】")
    learningProcess.machine_learning()

if __name__ == '__main__':
    main()