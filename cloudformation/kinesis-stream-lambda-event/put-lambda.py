import json
import boto3
import pickle


class User:
    def __init__(self):
        self.id = '001'
        self.name = 'tanaka'
        self.data = b'test001'


def lambda_handler(event, context):
    user = User()
    b = pickle.dumps(user)
    print(b)
    
    client = boto3.client('kinesis')
    response = client.put_record(
        Data=b,
        PartitionKey='123',
        StreamName='kinesis-test')
    print(response)
    
    shard = response['ShardId']
    sequence = response['SequenceNumber']
    
    it = client.get_shard_iterator(StreamName='kinesis-test', ShardId=shard, ShardIteratorType='AT_SEQUENCE_NUMBER', StartingSequenceNumber=sequence)
    shard_iterator = it['ShardIterator']
    get_response = client.get_records(ShardIterator=shard_iterator, Limit=1)
    print(get_response)
    
    record = get_response['Records'][0]['Data']
    print(record)
    
#   load_user = pickle.loads(record)
#   print(load_user.id)
#   print(load_user.name)
#   print(load_user.data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }