import boto3
from distutils.version import LooseVersion


client = boto3.client('lambda')


def get_latest_version(aliases):
    versions = list(map(lambda x: x['Name'], aliases))
    sorted_version = sorted(versions, key=LooseVersion, reverse=True)
    return sorted_version[0]


def handler(event, context):
    aliases = client.list_aliases(FunctionName=event['lambda_name'])['Aliases']
    if not aliases:
        raise ValueError('Alias dose not exists on the lambda function.')

    latest_version = get_latest_version(aliases)
    response = {"version": latest_version}
    response.update(event)
    print(response)

    return response


handler({'lambda_name': 'kinesis-test-read'}, {})

