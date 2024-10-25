# はじめに
Cosmos DBはデータをJSON形式で保存するNoSQLデータサービス。  
リソース構造は次のようになっている。
```
- Azure Cosmos DB アカウント
  - データベース
    - コンテナ
      - データ
```
つまり、データを入れるためにはコンテナまで作らなければならない。  
また、Cosmos DBでデータを扱う方法には、SQL API、MongoDB APIなど様々なAPIがある。  
SQLスタイルで記述できるので、以下のコマンドで`sql`が出てくることがある。

## Cosmos DBアカウントを作成
`--locations`には複数のリージョンを指定することができ、ゾーン冗長を持たせることができる。
```
az cosmosdb create -n <ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME> --locations regionName=japaneast failoverPriority=0
```

Cosmos DBアカウントの一覧表示
```
az cosmosdb list -g <RESOURCE_GROUP_NAME> -o table
```

Cosmos DBアカウントの削除
```
az cosmosdb delete -n <ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME> -y
```

## データベースを作成
```
az cosmosdb sql database create -a <ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME> -n <DATABASE_NAME>
```

SQLデータベースの一覧表示
```
az cosmosdb sql database list -a <ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME>
```

データベースの削除
```
az cosmosdb sql database delete -a <ACCOUNT_NAME> -n <DATABASE_NAME> -g <RESOURCE_GROUP_NAME> -y
```

## コンテナの作成
```
az cosmosdb sql container create -a <ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME> -d <DATABASE_NAME> -n <CONTAINER_NAME> -p '/pk' --max-throughput 4000
```
- Partition Keyとは
  - Partition Keyが同じコンテナは、同じ論理パーティションに割り当てられる。
  - Partition Keyはディレクトリと同じように`/pk`のように記述する。`/my/path`のように階層構造にすることもできる。
- Throughputとは
  - Cosmos DBでデータベース操作を実行するために必要な計算資源を表す指標で、「リクエストユニット(RU/s)」という単位で表される。1KBのドキュメントを読み込むのが1RU/s。
  - `--max-throughput`の最小値は4000RU/sで、この値を大きくするとCosmos DBにかかる料金が大きくなる。

コンテナの一覧表示
```
az cosmosdb sql container list -a <ACCOUNT_NAME> -d <DATABASE_NAME> -g <RESOURCE_GROUP_NAME> -o table
```

コンテナの削除
```
az cosmosdb sql container delete -a <ACCOUNT_NAME> -d <DATABASE_NAME> -g <RESOURCE_GROUP_NAME> -n <CONTAINER_NAME> -y
```

## 参考
[az_cosmosdbコマンド](https://learn.microsoft.com/ja-jp/cli/azure/cosmosdb?view=azure-cli-latest#az-cosmosdb-create)
[AzureCosmosDBリソースの管理](https://learn.microsoft.com/ja-jp/azure/cosmos-db/nosql/manage-with-cli)