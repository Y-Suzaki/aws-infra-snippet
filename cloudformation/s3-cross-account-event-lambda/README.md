# Setup
## Account Bにて
* IAM Roleの作成
    * lambda-execute-roleの作成
* Lambda Functionの作成
    * 3-event-cross-account
    * arn:aws:lambda:us-west-2:601373194128:function:3-event-cross-account
    ```
    import json
    import boto3
    import os
    import sys
    import uuid
    
    s3_client = boto3.client('s3')
    
    def lambda_handler(event, context):
        print(event)
        
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
            upload_path = '/tmp/resized-{}'.format(key)
     
            s3_client.download_file(bucket, key, download_path)
            with open(download_path) as var:
                print(var.read())
        
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }

    ```
* Lambda Permissionの追加
    ```
    aws lambda add-permission \
    --region us-west-2 \
    --function-name 3-event-cross-account \
    --statement-id cross-lambda \
    --principal s3.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:s3:::ys-s3-event-cross-account \
    --source-account 838023436798
    ```

## Account Aにて
* s3 Bcuket作成
    * ys-s3-event-cross-account
* s3 event作成
    * s3-create-cross-account-lambda
    * Events
        * All object create events
    * Lambda Arn
        * arn:aws:lambda:us-west-2:601373194128:function:3-event-cross-account
     * Bucket Policyの付与
         ```
         {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "GetObject",
              "Action": [
                "s3:GetObject"
              ],
              "Effect": "Allow",
              "Resource": "arn:aws:s3:::ys-s3-event-cross-account/*",
              "Principal": {
                "AWS": "601373194128"
              }
            },
            {
              "Sid": "ListBucket",
              "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket"
              ],
              "Effect": "Allow",
              "Resource": "arn:aws:s3:::ys-s3-event-cross-account",
              "Principal": {
                "AWS": "601373194128"
              }
            }
          ]
        }
         ```