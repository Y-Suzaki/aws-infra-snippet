import boto3
import json

# JSONが複数格納されているファイルを分割する

BUCKET = ''
KEY = ''

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET)
obj = bucket.Object(KEY)

# byte配列
bytes = obj.get()['Body'].read()
json_str = bytes.decode()

decoder = json.JSONDecoder()

while len(json_str) > 0:
    record, index = decoder.raw_decode(json_str)
    json_str = json_str[index:]
    print('******************************')
    print('next index: {}'.format(index))
    print(record)



