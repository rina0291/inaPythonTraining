import urllib3
import sys
from bs4 import BeautifulSoup


# WEBスクレイピング処理（TOTOサイトから過去の開催回取得）
def get_past_toto(year):
    # URL指定(TOTOサイト)
    url = "https://store.toto-dream.com/dcs/subos/screen/pi04/spin011/PGSPIN01101LnkSeasonLotResultLsttoto.form?meetingFiscalYear=" + year 
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
