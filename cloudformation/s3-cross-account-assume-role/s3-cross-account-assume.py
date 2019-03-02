import json
import os
import boto3

# Assume Roleを使用して取得する別アカウントのRole名
ROLE = 'arn:aws:iam::{}:role/ys-dev-web-s3-role'.format(os.environ['ASSUME_ACCOUNT_ID'])
LOCALE_PATH = '/tmp/assume.txt'

sts_client = boto3.client('sts')

def lambda_handler(event, context):
    with open(LOCALE_PATH, mode='w') as f:
        f.write('@@@@@@@@')

    response = sts_client.assume_role(
        RoleArn=ROLE,
        RoleSessionName='test'
    )
    credentials=response['Credentials']

    s3_client = boto3.resource(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'])

    bucket = s3_client.Bucket(os.environ['S3_BUCKET'])
    bucket.upload_file(LOCALE_PATH, 'assume.txt')
