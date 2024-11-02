## はじめに
Azure SQL serverは複数のデータベースをホストできる論理サーバーである。  
リソース構造は次のようになっている。
```
- Azure SQL server
  - SQL database
    - Table
```

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
- `--sample-name`: AdventureWorksLTを指定すると、サンプルデータをインポートできる。

## データベースの中身の確認
最も手軽な方法はAzure portalのデータベースリソースの中にある、Query editorを使うことである。  
ただし、上記の設定ではファイアウォールによりアクセスできないので、自分のPCからアクセスできるように変更する。

まず、グローバルIPv4アドレスを取得する
```
curl -4 ifconfig.me
```
得られたIPアドレスを使って新しいファイアウォールを作成する
```
az sql server firewall-rule create -n <RULE_NAME> -g <RESOURCE_GROUP_NAME> -s <SERVER_NAME> --start-ip-address <YOUR_IP_ADDRESS> --end-ip-address <YOUR_IP_ADDRESS>
```
変更が終わって5分程度経過するとファイアウォールの設定が反映される。  
Query editorで`SQL serverの作成`で作った管理者のユーザ名とパスワードを使ってログインできる。  
後は[Query editorリファレンス](https://learn.microsoft.com/ja-jp/azure/azure-sql/database/query-editor?view=azuresql)参照。

また、Azure SQL Databaseでは一部SQL文の書き方が異なる。[公式ドキュメント](https://learn.microsoft.com/en-gb/azure/azure-sql/database/transact-sql-tsql-differences-sql-server?view=azuresql)に詳細が記載されている。

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