#!/usr/bin/env bash

aws cloudformation package \
  --template-file devide-json-stream-sam.yaml \
  --output-template-file aws-sam-deploy.yaml \
  --s3-bucket ys-dev-web-kinesis-firehose-dev \
  --region us-west-2 \
  --profile default

aws cloudformation deploy \
  --template-file aws-sam-deploy.yaml \
  --stack-name aws-sam-deploy \
  --capabilities CAPABILITY_IAM \
  --region us-west-2 \
  --profile default

echo "** All complete! **"