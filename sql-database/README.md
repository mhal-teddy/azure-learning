## はじめに
Azure SQL serverは複数のデータベースをホストできる論理サーバーである。  
つまり、最初に`az sql server`コマンドでSQL server全体に関する設定を行った後、`az sql db`コマンドで個々のデータベースに関する設定を行う。

## SQL serverの作成
```
az sql server create -n <SERVER_NAME> -l <LOCATION> -g <RESOURCE_GROUP_NAME> -u <ADMIN_USER_NAME> -p <ADMIN_PASSWORD>
```
`ADMIN_USER_NAME`と`ADMIN_PASSWORD`は自由に決めることができる。ただし、パスワードは[パスワードポリシー](https://learn.microsoft.com/ja-jp/sql/relational-databases/security/password-policy?view=sql-server-ver16)を満たす必要がある。

サーバーの一覧は次のコマンドで確認できる。
```
az sql server list -g <RESOURCE_GROUP_NAME> -o table
```

サーバーを作ったら、ファイアウォールを設定する
```
az sql server firewall-rule create -n <RULE_NAME> -g <RESOURCE_GROUP_NAME> -s <SERVER_NAME> --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0
```
IP Addressを`0.0.0.0`に設定することで、すべてのAzureサービスからのアクセスが可能になる。

## データベースの作成
```
az sql db create -n <DATABASE_NAME> -g <RESOURCE_GROUP_NAME> -s <SERVER_NAME> -e GeneralPurpose -f Gen5 -c 2 -z false
```
- `--edition -e`: Database Editionとはデータベースの構成のことで、機能や価格が異なる。`az sql db list-editions -l <LOCATION> -o table`でEditionの一覧を取得できる。
  - GeneralPurpose: 仮想コアベースのモデルでスケーラブルであることが特徴
- `--family -f`: Editionを仮想コアベースにした時に設定する。使用する仮想マシンの世代を指定する。基本的には新しい世代が推奨される。
- `--capacity -c`: 仮想コアの数。
- `--zone-redundant -z`: ゾーン冗長を有効にするか。デフォルトはtrue。

## データベースの削除
```
az sql db delete -n <DATABASE_NAME> -g <RESOURCE_GROUP_NAME> -s <SERVER_NAME> -y
```

## SQL serverの削除
```
az sql server delete -n <SERVER_NAME> -g <RESOURCE_GROUP_NAME> -y
```

## 参考
[Azure CLIでデータベースを作成](https://learn.microsoft.com/ja-jp/azure/azure-sql/database/scripts/create-and-configure-database-cli?view=azuresql)

[az sql serverコマンド](https://learn.microsoft.com/ja-jp/cli/azure/sql/server?view=azure-cli-latest#az-sql-server-list)