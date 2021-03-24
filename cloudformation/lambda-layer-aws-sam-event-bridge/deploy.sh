#!/usr/bin/env bash

s3_bucket="cf-templates-461spye58s2i-us-west-2"

# Generate a cloud-formation template from a sam template.
aws cloudformation package \
  --template-file aws-sam.yaml \
  --output-template-file aws-sam-deploy.yaml \
  --s3-bucket ${s3_bucket} \
  --s3-prefix serverless-function \
  --region us-west-2 \
  --profile default

# Deploy a lambda layer and lambda function with the generated template.
aws cloudformation deploy \
  --template-file aws-sam-deploy.yaml \
  --stack-name ys-dev-web-lambda-event-xray-sdk \
  --capabilities CAPABILITY_IAM \
  --region us-west-2 \
  --profile default

# Remove the uploaded s3 files.
aws s3 rm s3://${s3_bucket}/serverless-function/ \
  --region us-west-2 \
  --profile default \
  --recursive

# Remove the unnecessary local files and directory.
rm -f aws-sam-deploy.yaml
