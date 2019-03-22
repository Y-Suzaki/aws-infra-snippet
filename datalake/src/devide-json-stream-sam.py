import boto3
import json
import urllib.parse


def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.unquote(key)
    s3 = boto3.resource('s3')

    print(key)

    # ファイルのダウンロード
    download_bucket = s3.Bucket(bucket)
    file_path = '/tmp/' + key
    download_bucket.download_file(Key=key, Filename=file_path)

    with open(file_path, 'r') as f:
        json_str = f.read()

    # 改行付きのJSONデータに変換
    output_path = file_path + '_'
    with open(output_path, 'w') as f:
        while len(json_str) > 0:
            record, index = json.JSONDecoder().raw_decode(json_str)
            json_str = json_str[index:]
            f.write(json.dumps(record) + '\n')

    # ファイルのアップロード
    upload_bucket = s3.Bucket('ys-dev-web-kinesis-firehose-transformed')
    upload_bucket.upload_file(output_path, Key=key)
