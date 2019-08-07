import boto3

s3 = boto3.resource('s3')


def handler(event, context):
    uri = event['uri']
    life_cycle_days = event['life_cycle_days']
    s3_bucket = "ys-dev-web-glue-purquet-data"
    lifecycle = s3.BucketLifecycle(s3_bucket)

    lifecycle.put(LifecycleConfiguration={
        'Rules': [
            {
                'Expiration': {
                    'Days': life_cycle_days
                },
                'ID': 'all-expire',
                'Prefix': '',
                'Status': 'Enabled'
            }
        ]
    })

    response = {"version": "0-0-1"}
    response.update(event)

    return response


