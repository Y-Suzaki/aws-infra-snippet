## 概要
1. APIGatewayのPOSTデータをKinesis Firehose経由でs3に送信する。
1. FirehoseのカスタムPrefixを使い、s3にはHive形式のパスで保存する。
1. GlueのCrawlerを生成し、カタログデータを作成する。
1. Athenaでクエリを実行する。

## 環境構築
* APIGateway + Kinesis Firehose + s3の構築
    * [kinesis + s3](../cloudformation/kinesis-firehose-from-apigateway-to-s3/kinesis-firehose-to-s3.yaml)
    * [APIGateway](../cloudformation/kinesis-firehose-from-apigateway-to-s3/apigateway-to-kinesis-firehose.yaml)
    * Hive形式のカスタムPrefixがCloudFormationで指定できないため、手動で設定した。（Bugかも）
 
 ## s3にアップロードされたパスの確認
 以下に配置された。期待通りの動きとなる。
 ```
 ys-dev-web-kinesis-firehose-dev/firehose/year=2019/month=03/day=13/
 ```
 
 ## Crawlerの実行
 * AWS Glueのコンソールから、Crawlerを作成
 * OnDemandで即時実行
 * 以下のデータカタログが作成された。
     ```
     CREATE EXTERNAL TABLE `firehose`(
       `name` string COMMENT 'from deserializer', 
       `address` string COMMENT 'from deserializer', 
       `age` int COMMENT 'from deserializer')
     PARTITIONED BY ( 
       `year` string, 
       `month` string, 
       `day` string)
      ・・・
     ```
 
 ## Athenaでクエリ
 ```
 ```
 