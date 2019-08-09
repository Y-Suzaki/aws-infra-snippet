import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    table = dynamodb.Table('LogType')
    table.update_item(
        Key={'uri': event['uri']},
        ExpressionAttributeNames={"#st": "status"},
        UpdateExpression='set #st = :status',
        ExpressionAttributeValues={':status': event['status']}
    )
    return event

