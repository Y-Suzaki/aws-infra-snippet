## FargateにSSM Agentを導入するまで
1. Activation Codeの作成  
初回はServiceRoleが存在していないので、AWSコンソールから作成した。  
もしくは事前に`AmazonSSMManagedInstanceCore`を付与した自作のRoleを作成しておき、そのRoleを使用しても良い。
```
aws ssm create-activation \
    --description fargate-ops \
    --iam-role "service-role/AmazonEC2RunCommandRoleForManagedInstances" \
    --registration-limit 100000 \
    --default-instance-name step-server-on-fargate \
    --region us-west-2

{
    "ActivationId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "ActivationCode": "xxxxxxxxxxxxxxxxxxx"
}
```

2. Activation CodeをParameter Storeに保存  
後でCloudFormationのTaskDefinition定義に埋め込む。
```
$ aws ssm put-parameter --name "activation-id" \
    --value "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
    --type "SecureString" \
    --region us-west-2

$ aws ssm put-parameter --name "activation-code" \
    --value "xxxxxxxxxxxxxxxxxxx" \
    --type "SecureString" \
    --region us-west-2
```

3. docker build & push
```
$ docker build -t step-server .

$ aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin  {accounrId}.dkr.ecr.us-west-2.amazonaws.com

$ docker tag step-server:latest {accounrId}.dkr.ecr.us-west-2.amazonaws.com/step-server:latest

$ docker push step-server:latest {accounrId}.dkr.ecr.us-west-2.amazonaws.com/step-server:latest
```

4. CloudFormationでFargateの作成
```
aws cloudformation deploy \
    --template fargate.yml \
    --stack-name ys-dev-web-fargate \
    --capabilities CAPABILITY_NAMED_IAM
```
5. SSM Session Managerのコンソールからログイン

## 課題
* Activation Codeの有効期限が最大でも30日間のため、踏み台サーバーとして使用するには、自動更新＋SSM Parameter Storeに登録のような仕組みが必要。