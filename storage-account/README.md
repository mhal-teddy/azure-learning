## Storage account とは
ストレージアカウントは、Azure Storageの各種データサービス（Blob、Files、Queue、Tableなど）を統合し、それらを一元的に管理するためのコンテナとして機能する。

## 一覧表示
```
az storage account list -g ResourceGroupName -o table
```

## Storage accountの作成
```
az storage account create -n <STORAGE_ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME> -l <LOCATION> --sku Standard_LRS
```
SKUの詳細は[一覧](https://learn.microsoft.com/ja-jp/rest/api/storagerp/srp_sku_types)で参照できる。

## Storage accountの削除
```
az storage account delete -n <STORAGE_ACCOUNT_NAME> -g <RESOURCE_GROUP_NAME>
```

## 参考
[storage_account](https://learn.microsoft.com/ja-jp/cli/azure/storage/account?view=azure-cli-latest#az-storage-account-create)