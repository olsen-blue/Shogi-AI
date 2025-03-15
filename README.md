## 将棋AIの思考エンジン(個人開発)

### ファイル構成
```
my_engine.py  ← 将棋AIの思考エンジン
my_engine.sh  ← ShogiHome用の起動スクリプト
```

### 下記の機能を実装済み
- 盤面からの指し手の生成
- 指し手を盤面に対して適用する機能
- ランダム指し手生成機能
- 簡易的な評価関数機能
- ミニマックス法による探索アルゴリズム
https://ja.wikipedia.org/wiki/%E3%83%9F%E3%83%8B%E3%83%9E%E3%83%83%E3%82%AF%E3%82%B9%E6%B3%95

### メモ:
- USIというプロトコルを用いています
http://shogidokoro.starfree.jp/usi.html

- MacではPythonスクリプトを直接実行するために、
**シェルスクリプト（.shファイル）**を作り、ShogiHome(GUI)で登録します。
