# CloudFormation
## ECS
### ecs-service.yaml
* 注意点
    * 初回作成時、以下のエラーが発生してしまう。
    ```$xslt
    Unable to assume the service linked role. Please verify that the ECS service linked role exists. (Service: AmazonECS
    ```
    * Service Roleがないエラーだが、CloudFormationで同時作成も可能になったため、対応すること。
## CodePipeline
### codepipeline-with-s3-codebuild.yaml 
* 課題
    * CloudWatch Eventが設定できていない。
    * CloudFormationベースだとやっかいだったため。
### step-server-amazon-linux
* 課題
    * SSMエージェントを動作させる権限が足りていない。
    * ひとまず以下を直接アタッチすれば動作は可能。
        * AmazonEC2RoleforSSM
        * AmazonSSMFullAccess
