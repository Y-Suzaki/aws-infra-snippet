import json
import boto3
import pickle
import base64


class User:
    def __init__(self):
        self.id = '001'
        self.name = 'tanaka'
        self.data = b'test001'


def lambda_handler(event, context):
    
    records = event['Records']
    
    for record in records:
        b = record['kinesis']['data']
        print(b)
        decode = base64.b64decode(b)
        
        load_user = pickle.loads(decode)
        print(load_user.id)
        print(load_user.name)
        print(load_user.data)
    
#   load_user = pickle.loads(record)
#   print(load_user.id)
#   print(load_user.name)
#   print(load_user.data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
