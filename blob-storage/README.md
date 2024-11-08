# Blob storageの特徴
テキストデータやバイナリデータなどの非構造化データを格納することに最適化されている。

## リソース構造
次の3つのリソースが存在して、階層構造になっている。
- Storage account
  - Container
    - Blob

## Containerの作成
Containerに対してデータ操作を行うためには、共同作成者ロールを自分に割り当てなければならない。  
まず、Storage accountを作成していない場合は、[Storage account詳細](https://github.com/mhal-teddy/azure-learning/tree/main/storage-account)にしたがってアカウントを作成する。

次に、共同作成者ロールを割り当てるときにSubscription IDが必要になるので、コマンドで取得する。
```
az account show --query id
```

Storage accountとSubscription IDの準備ができたら、共同作成者ロールを割り当てる。
```
az ad signed-in-user show --query id -o tsv | az role assignment create --role "Storage Blob Data Contributor" --assignee @- --scope "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP_NAME>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT_NAME>"
```

割り当てられたら、次のコマンドでContainerを作成する
```
az storage container create --account-name <STORAGE_ACCOUNT_NAME> --name <CONTAINER_NAME> --auth-mode login
```

Container一覧の表示
```
az storage container list --account-name <STORAGE_ACCOUNT_NAME> --auth-mode login -o table
```

Containerの削除
```
az storage container delete --name <CONTAINER_NAME>
```

## ファイルのアップロード
`<FILE_NAME>`はローカルに存在するファイル名、`<BLOB_NAME>`はアップロードされたBlobの中での名前。
```
az storage blob upload --account-name <STORAGE_ACCOUNT_NAME> -c <CONTAINER_NAME> -f <FILE_NAME> -n <BLOB_NAME> --auth-mode login
```
