# mf-to-spreadsheet

MoneyForwardのデータをSpreadSheetに連携するスクリプト。

## バッチの実行

[MoneyForwardのデータ](https://moneyforward.com/cf)を`src.csv`の命名でダウンロードし、`src`配下に配置したら以下を実行する。

```sh
docker compose up
```

## コンテナへの接続

```sh
docker compose exec app bash
```

## コンテナの停止

```sh
docker compose down
```

## Reference

- [Google Spread Sheets に Pythonを用いてアクセスしてみた](https://qiita.com/164kondo/items/eec4d1d8fd7648217935)
