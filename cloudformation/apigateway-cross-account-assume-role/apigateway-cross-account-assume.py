import json
import os
import boto3
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

# Assume Roleを使用して取得する別アカウントのRole名
ROLE = 'arn:aws:iam::{}:role/ys-dev-web-apigateway-role'.format(os.environ['ASSUME_ACCOUNT_ID'])
APIGATEWAY_DOMAIN = os.environ['APIGATEWAY_DOMAIN']
API_URL = 'https://{}/prod/'.format(APIGATEWAY_DOMAIN)

sts_client = boto3.client('sts')

def lambda_handler(event, context):
    # stsにて、Lambda自身のRoleから一時認証情報を取得する
    response = sts_client.assume_role(
        RoleArn=ROLE,
        RoleSessionName='test'
    )
    credentials=response['Credentials']

    # HTTPリクエストで認証情報が送れるように、AWSRequestsAuthを使用する
    auth = AWSRequestsAuth(
        aws_access_key=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_token=credentials['SessionToken'],
        aws_host=APIGATEWAY_DOMAIN,
        aws_region='us-west-2',
        aws_service='execute-api')

    headers = {'x-amz-security-token':credentials['SessionToken']}

    response = requests.get(API_URL, auth=auth, headers=headers)
    print(response.json())
