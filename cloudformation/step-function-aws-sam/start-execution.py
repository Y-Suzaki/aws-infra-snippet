import boto3
from botocore.exceptions import ClientError
import json

step_function = boto3.client('stepfunctions')


class DataLakeStorageRepository:
    @staticmethod
    def create(uri: str):
        # TODO: 本来は環境変数から取得する
        step_function_arn = "arn:aws:states:us-west-2:838023436798:stateMachine:data-lake-control-delete-log-type"
        request = {"uri": uri}
        try:
            response = step_function.start_execution(stateMachineArn=step_function_arn, input=json.dumps(request))
            print(response)
        except ClientError as e:
            pass

    @staticmethod
    def delete(uri: str):
        pass


# Test
DataLakeStorageRepository.create("test-001")
