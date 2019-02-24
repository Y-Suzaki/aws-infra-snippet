import json
import boto3

client = boto3.client('servicediscovery')

def lambda_handler(event, context):
    instances = client.discover_instances(
        NamespaceName='sample-biz-system',
        ServiceName='test-application',
        QueryParameters={'env': 'dev'})

    return {
        "statusCode": 200,
        "body": json.dumps({
            'dynamodb-table': instances['Instances'][0]['InstanceId'],
        })
    }