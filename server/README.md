# docker commands

```
docker-compose up -d
docker-compose exec server bash
```

# `.env` ファイルの例

## AWS に関するの環境変数

```
CDK_DEFAULT_REGION=CDK_DEFAULT_REGION
AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
S3_BUCKET_NAME=S3_BUCKET_NAME
CDN_ORIGIN=https://CDN_DOMAIN.cloudfront.net
CLOUDFRONT_KEY_PAIR_ID=CLOUDFRONT_KEY_PAIR_ID
```

# 必要なパーミッション

- cloudfront
- S3 read

# index.py の役割

- 事前に登録した S3 のパスから CDN 署名付き URL を発行する
- 署名付き URL を`images.json`、`server/data`に保存

# TODO

## `images.json`の自動生成

有効期限が切れてしまうと、閲覧したいときにユーザが見れることができないのでバックエンドで`images.json`を更新するようにする

### 案 1

ミドルウェアに、`images.json`を更新する処理を配置する。もしくは、`images.json`更新用ページを作成する

#### 必要な AWS 構成サービス

- Lambda
- API Gateway
- AWS Secrets Manager
- S3

#### 課題・問題点

- AWS Secrets Manager に、非公開鍵を格納して Lambda で呼び出すこと処理の作成でつまづいている
- S3 時代をパブリックアクセスをオフかつ CloudFront で署名付きの設定をしているので、`images.json`だけ公開設定を緩めることになる
  　- バケットを分けることも考えられるが、冗長である

### 案 2

Rails とかを EC2 に配置して、API を作成する
-> ECS とかでもよさそう

#### 課題・問題点

- オーバースペックな気がする
- アプリケーションの稼働に見合ってない

### 案 3

このまま
