# Go言語のお勉強用

## Dockerについて

リポジトリ「dockersss」に入れてしまった。
当時はなんか「Dockerものは全部こっちのリポジトリに入れとこう」とかやってたんだけどさ。
全部のお勉強コンテナとかまで色々定義されてるから、今となってはめんどくさい。

というわけで移植した。
あんちょこは以下。項番とかは未修正。

## 3 : mySQL を触りたいので追加。

### 3-1 : 起動～中に入る

1. docker compose build mySQL
2. docker compose up -d mySQL
3. docker compose ps
4. docker compose exec mySQL bash

### 3-2 : mySQL を動かす

1. mysql -u docker -pdocker
2. show databases;
3. show tables;
4. use test_db;

3.はあると思うけど、4 は 0 件のハズ。

### 3-3 : A5m2 で遊ぶ

1. 3-2 に接続する。とりあえずまずは root/root で。
2. mysql_db とかいうあたりの テーブル users で docker ユーザーの権限を全部 root とお揃いにする。
3. docker/docker で入り直す。
4. 好きに遊ぶ。



mysql -h 127.0.0.1 -u docker test_db -p < createTable.sql