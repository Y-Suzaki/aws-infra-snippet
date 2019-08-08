import boto3
from distutils.version import LooseVersion


client = boto3.client('lambda')


def get_latest_version(versions):
    sorted_version = sorted(versions, key=LooseVersion, reverse=True)
    print(sorted_version)



def handler(event, context):
    aliases = client.list_aliases(FunctionName=event['lambda_name'])['Aliases']
    if not aliases:
        raise ValueError('Alias dose not exists on the lambda function.')

    versions = list(map(lambda x: x['Name'], aliases))
    latest_version = get_latest_version(versions)

    response = {"version": latest_version}
    response.update(event)

    return response


handler({'lambda_name': 'kinesis-test-read'}, {})

