# データレイクの基礎のチュートリアル
## AWSの公式ブログ
* https://aws.amazon.com/jp/blogs/news/build-a-data-lake-foundation-with-aws-glue-and-amazon-s3/

## Crawlerの作成
### Data catalogメニューの説明
* Tables
    * AthenaでCreateしたTableも表示される
    * 手動でTableを追加したパターンと言える
* Crawlers
    * Crawlerに自動定義してもらう時はこっち
    * Crawler名、Storage（s3）、IAM Roleなどを指定していく
    * 定期実行も可能だが、チュートリアルではオンデマンドで実施
### チュートリアルの元データ
```
VendorID,lpep_pickup_datetime,lpep_dropoff_datetime,store_and_fwd_flag,RatecodeID,PULocationID,DOLocationID,passenger_count,trip_distance,fare_amount,extra,mta_tax,tip_amount,tolls_amount,ehail_fee,improvement_
surcharge,total_amount,payment_type,trip_type

2,2017-01-01 00:01:15,2017-01-01 00:11:05,N,1,42,166,1,1.71,9,0,0.5,0,0,,0.3,9.8,2,1
2,2017-01-01 00:03:34,2017-01-01 00:09:00,N,1,75,74,1,1.44,6.5,0.5,0.5,0,0,,0.3,7.8,2,1
```

### 自動生成されたTable
* 今回はCSVにヘッダがあるため、カラム名はそこから付与される
* データ型は自動で判別されている

### Athena経由のクエリ
* ここまで作成が終わると、Athenaからクエリができる

## ETL（CSVからParquet形式に変換する）
### Parquet ？
* 列志向でデータ処理ができるフォーマット
* 高速化やスキャンするデータ量の削減になるらしい
    * カラムを絞ってクエリするのが良い
    * 全カラムを対象にするなら、CSVのままで良い
### 手順
* チュートリアルに沿って進めると、ETL処理のPythonコードが自動生成される
    * 変換元のデータは上記でCrawlerが自動生成したもの
    * 出力先s3 bucketに権限がないため、Policyをアタッチしておくこと
* 自動生成されたJOBを実行すると、Purquet形式に変換されたデータが、s3にアップロードされる

### Purquet形式のデータを読み込ませる
* Purquet形式のファイルが格納されているs3にCrawlerを実行
    * 手順は最初にやったものと同じ
    * この時点で、CSV用とPurquet形式の２つのテーブルが存在する
* 自動生成されたData Catalogに対し、Athenaからスキャンできる
