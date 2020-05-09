#!/bin/bash -e

s3_bucket="ys-dev-web-app-deploy"

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
  --template-file aws-sam.yaml \
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

rm -rf aws-sam-deploy.yaml lambda.zip lambda/
