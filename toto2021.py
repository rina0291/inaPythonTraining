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

    # toto年度別全開催回数を取得する
    toto_no_info = scrapingProcess.get_past_toto("2022") + scrapingProcess.get_past_toto("2021")

    cnt=0

    # 学習用CSV作成処理
    print("【学習用CSV作成中】")
    for no in toto_no_info:
        print("第"+str(no)+"回処理中")
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