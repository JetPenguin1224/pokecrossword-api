
# pokecrossword-api

FastAPIを使用して構築されたAPIサーバーです。ポケモンの名前限定のクロスワードパズルの解決を行います。

#### セットアップ

1. 必要な依存関係をインストールします。

    ```bash
    pip install -r requirements.txt
    ```

2. サーバーを起動します。

    ```bash
    uvicorn app.main:app --reload
    ```

#### テスト

テストを実行するには、以下のコマンドを使用します。

```bash
pytest
```

#### APIの呼び出し方

##### ルートエンドポイント

- **GET /**

    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/' \
      -H 'accept: application/json'
    ```

##### パズル解決エンドポイント

- **POST /solve**

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/solve' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
        "dimensions": {
          "rows": 4,
          "cols": 5
        },
        "binaryGrid": [
          [1, 1, 1, 1, 1],
          [0, 1, 0, 0, 0],
          [0, 1, 0, 0, 0],
          [0, 1, 0, 0, 0]
        ],
        "charGrid": [
          ["ピ", "", "", "ュ", "ウ"],
          ["", "", "", "", ""],
          ["", "ゴ", "", "", ""],
          ["", "ン", "", "", ""],
        ]
      }'
    ```

##### レスポンス
    ```javascript
    {
        "solved" : true,
        "grid" : [
          ["ピ", "カ", "チ", "ュ", "ウ"],
          ["#", "ビ", "#", "#", "#"],
          ["#", "ゴ", "#", "#", "#"],
          ["#", "ン", "#", "#", "#"],
        ]
    }
    ```
    何も入らないセルには#が入ります。

