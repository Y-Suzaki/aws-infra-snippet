import boto3
import json

def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    file_path = '/tmp/' + key
    bucket.download_file(Key=key, Filename=file_path)

    with open(file_path, 'r') as f:
        json_str = f.read()

    ouput_path = file_path + '_'

    with open(ouput_path, 'w') as f:
        while len(json_str) > 0:
            record, index = json.JSONDecoder().raw_decode(json_str)
            json_str = json_str[index:]
            print(record)
            f.write(record)

    bucket.upload_file(ouput_path, Key=ouput_path)