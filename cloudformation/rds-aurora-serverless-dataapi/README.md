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

### 3. テストデータの作成
AWSコンソールのQuery Editorから実行。

テーブル作成
```mysql
create database test;
use test;

create table department (
  id int(11) auto_increment not null,
  name varchar(30),
  primary key(id)
);

create table user (
  id int(11) auto_increment not null,
  name varchar(30) not null,
  department_id int(11),
  foreign key fk_department(department_id) references department(id),
  primary key(id)
);
```

テストデータ投入
```mysql
insert into department (name) values("human resource");
insert into department (name) values("service development");
insert into department (name) values("sales");
insert into department (name) values("production");

insert into user (name, department_id) values("akiyama", 1);
insert into user (name, department_id) values("ueno", 1);
insert into user (name, department_id) values("katagiri", 2);
insert into user (name, department_id) values("kondou", 2);
insert into user (name, department_id) values("tanaka", 2);
insert into user (name, department_id) values("satou", 3);
insert into user (name, department_id) values("ikeda", 3);
insert into user (name, department_id) values("miura", 3);
insert into user (name, department_id) values("nomura", 3);
```

### 4. Python boto3を使ってDataAPI実行
[lambda_handler.py](./lambda_handler.py) を参照。

## 参考URL
* [AWS公式 Aurora Serverless の Data API の使用
  ](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/data-api.html)