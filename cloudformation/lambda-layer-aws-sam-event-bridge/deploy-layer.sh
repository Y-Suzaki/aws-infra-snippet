#!/usr/bin/env bash

s3_bucket="cf-templates-461spye58s2i-us-west-2"

# Create a zip file of lambda layer. The directory path must be python/logger/lambda_json_logger.py.
mkdir -p python
cp -r xray-sdk/* python
cd python
py -m pip install -r requirements.txt -t .
cd ..
zip -r lambda-layer.zip python


# Generate a cloud-formation template from a sam template.
aws cloudformation package \
  --template-file aws-sam-layer.yaml \
  --output-template-file aws-sam-layer-deploy.yaml \
  --s3-bucket ${s3_bucket} \
  --s3-prefix serverless-function \
  --region us-west-2 \
  --profile default

# Deploy a lambda layer and lambda function with the generated template.
aws cloudformation deploy \
  --template-file aws-sam-layer-deploy.yaml \
  --stack-name ys-dev-web-lambda-layer-xray-sdk \
  --capabilities CAPABILITY_IAM \
  --region us-west-2 \
  --profile default

# Remove the uploaded s3 files.
aws s3 rm s3://${s3_bucket}/serverless-function/ \
  --region us-west-2 \
  --profile default \
  --recursive

# Remove the unnecessary local files and directory.
rm -rf python
rm -f aws-sam-layer-deploy.yaml lambda-layer.zip
