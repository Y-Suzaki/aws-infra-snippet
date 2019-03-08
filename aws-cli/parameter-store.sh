#!/usr/bin/env bash

echo "AWS Parameter Store"

# デプロイバージョンの登録
aws ssm put-parameter \
  --name "/service/application/deploy-version" \
  --type "String"  \
  --value "v0-0-1" \
  --overwrite \
  --region "us-west-2"

# デプロイバージョンの取得
# jqコマンドで値のみ取得（別途インストールが必要）
aws ssm get-parameter \
  --name "/service/application/deploy-version" \
  --no-with-decryption \
  --region us-west-2 \
| jq -r .Parameter.Value > deploy_version

cat deploy_version
