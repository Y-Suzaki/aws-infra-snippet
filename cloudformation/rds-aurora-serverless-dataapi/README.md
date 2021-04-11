## Aurora Serverlessで、DataAPIを使う
### 1. CloudFormationで、Aurora Serverless構築
* [base-rds-aurora-severless.yml](../base-rds-aurora-severless.yml) を利用して、構築する。
* リージョンは、`us-west-2`を使用。

### 2. DataAPIを有効化
CloudFormationではできないため、AWS CLIで有効化する。
```
aws rds modify-db-cluster \
    --db-cluster-identifier ys-dev-web-rds-aurora-serverless-dev \
    --region us-west-2 \
    --enable-http-endpoint
```