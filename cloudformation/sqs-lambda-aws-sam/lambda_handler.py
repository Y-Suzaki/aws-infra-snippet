import json
import os
from retry import retry

# SQSから送られてくるEvent
# {
#     "Records": [
#         {
#             "messageId": "90cd08d8-4dda-472d-846c-a4790fcf170a",
#             "receiptHandle": "AQEBp2GaAbyNvpNcDrxZIP2WWJkSfBmKcaCrDjI0cRxOGzmHbWsESw1kiC2GmUQBdOfsRXlDw3nkeUDfkZrhPIgKpt/XhpqUlr3fUILT+c/W55/q0vVfgdcHsYCJJdU3E21sVR+7I4DcjFVKQfG8JjMlMG+yGnyxAFsNqb+dOXPzpZ1+06RTiNFIqckOGCTwVsHMerACaUmetmrkzu/gErnW61xwQnRn9hXRJKtrudnIKq2kqxq2wzLYiBIKjWBMg/gOFsMa8PDfTqexJZcTBbePA5O9yTfaqobOZxvgtkL9UEI=",
#             "body": "TEST",
#             "attributes": {
#                 "ApproximateReceiveCount": "1",
#                 "SentTimestamp": "1588943836863",
#                 "SequenceNumber": "18853513695946480128",
#                 "MessageGroupId": "01234",
#                 "SenderId": "AIDAIVJV5X5ZFV63K675S",
#                 "MessageDeduplicationId": "01234",
#                 "ApproximateFirstReceiveTimestamp": "1588943836863"
#             },
#             "messageAttributes": {},
#             "md5OfBody": "033bd94b1168d7e4f0d644c3c95e35bf",
#             "eventSource": "aws:sqs",
#             "eventSourceARN": "arn:aws:sqs:us-west-2:838023436798:lambda-event-output-dev.fifo",
#             "awsRegion": "us-west-2"
#         }
#     ]
# }

class CommunicationError(Exception):
    pass


@retry(CommunicationError, tries=3, delay=1, backoff=2)
def send(body: dict):
    print(body)
    raise CommunicationError('Error!!!')


def handler(event, context):
    # 設計上必ず1件ずつ送られてくることを前提にしているため、
    # SQSのBatch Sizeを変更する場合は、本関数の変更も必要。
    print(event)
    retry_limit = os.environ['RETRY_LIMIT']
    record = event['Records'][0]
    body = record['body']
    receive_count = record['attributes']['ApproximateReceiveCount']

    if receive_count < retry_limit:
        raise Exception(f'Because of being less than retry limit, this event will be retry. {receive_count}')
    else:
        print(f'Because of reaching retry limit, this event will be discarded. {body} {receive_count}')

    return event


try:
    send({'type': 'freeword'})
except Exception as e:
    print(type(e))
    print(e)
