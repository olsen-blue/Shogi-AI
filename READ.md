```
将棋AI(自作)/  ← プロジェクトフォルダ
├── my_engine.py  ← Pythonの思考エンジン
├── my_engine.sh  ← ShogiHome用の起動スクリプト
└── README.md  ← 説明ファイル（あってもなくてもOK）
```

USIというプロトコルを用いています
http://shogidokoro.starfree.jp/usi.html

MacではPythonスクリプトを直接実行するために、
**シェルスクリプト（.shファイル）**を作り、ShogiHome(GUI)で登録します

(追記)250313
ランダム指し手生成機能、簡易的な評価関数機能を追加実装しました。