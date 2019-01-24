# CloudFormation
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
