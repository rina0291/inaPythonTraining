import pandas as pd
from sklearn import tree

def machine_learning():
    # CSV読み込み
    train = pd.read_csv("newOutput.csv",encoding='Shift_JIS')
    test =  pd.read_csv("yosou.csv",encoding='Shift_JIS')
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

