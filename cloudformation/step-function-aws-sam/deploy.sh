#!/bin/bash -e

s3_bucket="ys-dev-web-codepipeline-artifacts"

echo "** Start to deploy and build. **"

echo "Build serverless function..."
aws cloudformation package \
  --template-file aws-sam-delete.yaml \
  --output-template-file aws-sam-deploy.yaml \
  --s3-bucket ${s3_bucket} \
  --s3-prefix serverless-function \
  --region us-west-2 \
  --profile default

echo "Deploy serverless function..."
aws cloudformation deploy \
  --template-file aws-sam-deploy.yaml \
  --stack-name serverless-function \
  --capabilities CAPABILITY_IAM \
  --region us-west-2 \
  --profile default

echo "** All complete! **"
aws s3 rm s3://${s3_bucket}/serverless-function/ \
  --region us-west-2 \
  --profile default \
  --recursive

rm -f aws-sam-deploy.yaml
