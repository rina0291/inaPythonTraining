import csv

# CSVクリア
def csv_clear():
    with open("newOutput.csv", 'a') as f:
        f.truncate(0)


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