# ECR関連
### コマンド
* ECRログイン
```$xslt
aws ecr get-login --region us-west-2 --no-include-email | sh
```
* BuildからPushまで
```$xslt
docker build -t nginx:latest .
docker tag nginx:latest {AWS Account Id}.dkr.ecr.us-west-2.amazonaws.com/nginx:latest
docker push {AWS Account Id}.dkr.ecr.us-west-2.amazonaws.com/nginx:latest
```