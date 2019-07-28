# Setup
## Download npm
```
npm install -g s3rver
```

# How to Use
## Run server
```
mkdir -p data
s3rver -d ./data
```

## Create AWS Configure
```
{
  accessKeyId: "S3RVER",
  secretAccessKey: "S3RVER",
}
```

## In Case of AWS CLI
### Create Bucket
```
aws s3 mb s3://test --endpoint-url "http://localhost:4568" --profile s3rver
```
### Put Object
```
```
### Get Object
```
```
### Copy Object
```
aws s3 cp aa.txt s3://test --endpoint-url "http://localhost:4568" --profile s3rver
```
