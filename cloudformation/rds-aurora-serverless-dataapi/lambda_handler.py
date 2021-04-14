import boto3
import os
import json
from typing import List


def execute_select_sql(sql):
    client = boto3.client('rds-data', region_name='us-west-2')
    args = {
        'secretArn': os.environ['SECRET_ARN'],
        'resourceArn': os.environ['DB_CLUSTER_ARN'],
        'sql': sql,
        'database': 'test'
    }

    response = client.execute_statement(**args)
    return response['records']


def execute_find_user_with_placeholder(user_name: str):
    client = boto3.client('rds-data', region_name='us-west-2')
    args = {
        'secretArn': os.environ['SECRET_ARN'],
        'resourceArn': os.environ['DB_CLUSTER_ARN'],
        'sql': 'select * from user where name = :name',
        'parameters': [
            {'name': 'name', 'value': {'stringValue': user_name}}
        ],
        'database': 'test'
    }

    response = client.execute_statement(**args)
    return response['records']


def _start_transaction(client):
    args = {
        'secretArn': os.environ['SECRET_ARN'],
        'resourceArn': os.environ['DB_CLUSTER_ARN'],
        'database': 'test'
    }
    return client.begin_transaction(**args)


def _commit_transaction(client, tr):
    args = {
        'secretArn': os.environ['SECRET_ARN'],
        'resourceArn': os.environ['DB_CLUSTER_ARN'],
        'transactionId': tr['transactionId']
    }
    return client.commit_transaction(**args)


def _rollback_transaction(client, tr):
    args = {
        'secretArn': os.environ['SECRET_ARN'],
        'resourceArn': os.environ['DB_CLUSTER_ARN'],
        'transactionId': tr['transactionId']
    }
    return client.rollback_transaction(**args)


def execute_transaction_sql(sql):
    client = boto3.client('rds-data', region_name='us-west-2')
    tr = _start_transaction(client)

    try:
        args = {
            'secretArn': os.environ['SECRET_ARN'],
            'resourceArn': os.environ['DB_CLUSTER_ARN'],
            'database': 'test',
            'sql': sql,
            'transactionId': tr['transactionId']
        }
        response = client.execute_statement(**args)

        _commit_transaction(client, tr)
        return response['numberOfRecordsUpdated']
    except Exception as e:
        _rollback_transaction(client, tr)


def execute_transaction_multiple_sql(users: List):
    client = boto3.client('rds-data', region_name='us-west-2')
    tr = _start_transaction(client)
    parameters = []

    for user in users:
        parameters.append([
            {
                'name': 'name',
                'value': {'stringValue': user[0]}
            },
            {
                'name': 'department_id',
                'value': {'longValue': user[1]}
            }
        ])

    try:
        args = {
            'secretArn': os.environ['SECRET_ARN'],
            'resourceArn': os.environ['DB_CLUSTER_ARN'],
            'database': 'test',
            'sql': 'insert into user (name, department_id) values(:name, :department_id)',
            'parameterSets': parameters,
            'transactionId': tr['transactionId']
        }
        response = client.batch_execute_statement(**args)

        _commit_transaction(client, tr)
        return response['updateResults']
    except Exception as e:
        _rollback_transaction(client, tr)


def handler(event, context):
    print('Use DataAPI on Aurora Serverless')
    # Normal Query
    # response = execute_select_sql('select * from user')
    # print(json.dumps(response, indent=2))

    # Join Query
    # response = execute_select_sql('select user.name from user inner join department on user.department_id = department.id where department.id = 3')
    # print(json.dumps(response, indent=2))

    # Transaction Query
    # response = execute_transaction_sql('insert into department(name) values ("iba")')
    # print(response)

    # Transaction Query Multiple Query
    response = execute_transaction_multiple_sql([
        ['aikawa', 1],
        ['ishikawa', 2],
        ['kitagawa', 3]
    ])
    print(response)

    # Normal Query using placeholder
    # response = execute_find_user_with_placeholder('katagiri')
    # print(response)


if __name__ == "__main__":
    handler(None, None)
