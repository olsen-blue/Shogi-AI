ファイル構成
```
my_engine.py  ← 将棋AIの思考エンジン
my_engine.sh  ← ShogiHome用の起動スクリプト
```

USIというプロトコルを用いています
http://shogidokoro.starfree.jp/usi.html

MacではPythonスクリプトを直接実行するために、
**シェルスクリプト（.shファイル）**を作り、ShogiHome(GUI)で登録します

盤面からの指し手の生成・指し手を盤面に対して適用する機能を実装済み。

(追記)250313
ランダム指し手生成機能、簡易的な評価関数機能を追加実装済み。
