#!/bin/bash -e

s3_bucket="cf-templates-461spye58s2i-us-west-2"

echo "** Start to deploy and build. **"

echo "Zip python codes"
mkdir -p lambda
cp lambda_handler.py requirements.txt lambda/
cd lambda
pip install -r requirements.txt -t .
zip -r ../lambda.zip ./*
cd ..

echo "Build serverless function..."
aws cloudformation package \
  --template-file aws-sam.yml \
  --output-template-file aws-sam-deploy.yml \
  --s3-bucket ${s3_bucket} \
  --s3-prefix serverless-function \
  --region us-west-2 \
  --profile default

echo "Deploy serverless function..."
aws cloudformation deploy \
  --template-file aws-sam-deploy.yml \
  --stack-name serverless-function \
  --capabilities CAPABILITY_IAM \
  --region us-west-2 \
  --profile default

echo "** All complete! **"
aws s3 rm s3://${s3_bucket}/serverless-function/ \
  --region us-west-2 \
  --profile default \
  --recursive

rm -rf aws-sam-deploy.yaml lambda.zip lambda/
