## 概要
CloudFrontのアクセスログを、AWS Athenaで分析する。

## 環境構築
[base-cloudfront.yaml](../base-cloudfront.yaml)

## Athenaの実施手順
#### テーブルの作成
```
CREATE EXTERNAL TABLE `cloudfront_logs`(
  `date` date, 
  `time` string, 
  `location` string, 
  `bytes` bigint, 
  `requestip` string, 
  `method` string, 
  `host` string, 
  `uri` string, 
  `status` int, 
  `referrer` string, 
  `useragent` string, 
  `querystring` string, 
  `cookie` string, 
  `resulttype` string, 
  `requestid` string, 
  `hostheader` string, 
  `requestprotocol` string, 
  `requestbytes` bigint, 
  `timetaken` float, 
  `xforwardedfor` string, 
  `sslprotocol` string, 
  `sslcipher` string, 
  `responseresulttype` string, 
  `httpversion` string, 
  `filestatus` string, 
  `encryptedfields` int)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://ys-dev-web-cloudfront-log-dev/'
TBLPROPERTIES (
  'skip.header.line.count'='0',
  'has_encrypted_data'='false'
);  
```

#### select文の発行
過去1日分のログを対象に、エラー情報を取得
```
SELECT uri,
         status,
         referrer,
         count(*)
FROM cloudfront_logs
WHERE responseresulttype = 'Error'
        AND date > now() - interval '1' day
GROUP BY  uri, status, referrer
```

## パーティションの分割
#### 課題
* CloudFrontのログは大量になるため、全ログをスキャンすることは現実的ではない
* パーティション分割が必須となる
#### s3のパスに日付を付与
* 「dt=2019-03-07」配下にログを移動させる
* テスト用に同じデータを「dt=2019-03-08」にもコピーしておく
* 実環境では、s3 event + Lambdaで自動化するなどが必要
```
s3://ys-dev-web-cloudfront-log-dev/dt=2019-03-07/xxx
s3://ys-dev-web-cloudfront-log-dev/dt=2019-03-08/xxx
```

#### テーブルの再作成
```
CREATE EXTERNAL TABLE `cloudfront_logs`(
  `date` date, 
  `time` string, 
  `location` string, 
  `bytes` bigint, 
  `requestip` string, 
  `method` string, 
  `host` string, 
  `uri` string, 
  `status` int, 
  `referrer` string, 
  `useragent` string, 
  `querystring` string, 
  `cookie` string, 
  `resulttype` string, 
  `requestid` string, 
  `hostheader` string, 
  `requestprotocol` string, 
  `requestbytes` bigint, 
  `timetaken` float, 
  `xforwardedfor` string, 
  `sslprotocol` string, 
  `sslcipher` string, 
  `responseresulttype` string, 
  `httpversion` string, 
  `filestatus` string, 
  `encryptedfields` int) 
   PARTITIONED BY (dt string)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://ys-dev-web-cloudfront-log-dev/'
TBLPROPERTIES (
  'skip.header.line.count'='0',
  'has_encrypted_data'='false'
);
```

#### パーティションのロード
```
MSCK REPAIR TABLE cloudfront_logs
```
上記も1日1回実施する必要があるため、自動化が必要

#### select文の発行
```
SELECT uri,
         status,
         referrer,
         count(*)
FROM cloudfront_logs
WHERE responseresulttype = 'Error'
        AND dt = '2019-03-07'
GROUP BY  uri, status, referrer
```
実行結果： (Run time: 3.86 seconds, Data scanned: 7.6 KB)

```
SELECT uri,
         status,
         referrer,
         count(*)
FROM cloudfront_logs
WHERE responseresulttype = 'Error'
        AND dt >= '2019-03-07'
GROUP BY  uri, status, referrer
```
実行結果： (Run time: 2.12 seconds, Data scanned: 15.21 KB)
* 日付を2日分にしたことで、スキャン量も倍になっていることが分かる