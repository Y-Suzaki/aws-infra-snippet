import json

from aws_xray_sdk.core import patch_all
import boto3

patch_all()
client = boto3.client('events')

def handler(event, context):

    res = client.put_events(
        Entries=[
            {
                'Source': 'ys.dev.web.x-ray-test',
                'Resources': [],
                'DetailType': 'X-Ray-Test',
                'Detail': json.dumps({
                    'key': 'val'
                })
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }
