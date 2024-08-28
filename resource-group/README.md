## Resource groupとは
- リソースの整理と管理: リソースグループは、仮想マシン、データベース、ストレージアカウントなど、関連するAzureリソースをまとめて管理するための「箱」や「フォルダ」として機能します。
- ライフサイクルの共有: 同じリソースグループ内のリソースは、同じライフサイクルを共有し、一緒にデプロイ、更新、削除されます。異なるライフサイクルを持つリソースは別のリソースグループに配置することが推奨されます。
- アクセス制御とポリシー適用: リソースグループは、アクセス制御（Azure RBAC）やポリシーの適用範囲としても使用され、管理の効率化に寄与します。
- タグ付け: リソースグループにはタグを適用することができ、リソースの分類やコスト分析、ポリシーの自動適用に利用されます。

## Resource groupの作成
```
az group create --name ResourceGroupName --location LocationName
```
`ResourceGroupName`には任意の名前をつける。使用可能な`LocationName`の一覧は次のコマンドで確認できる。
```
az account list-locations -o table
```

## Resource groupの情報を確認
```
az group show --name ResourceGroupName
```

## Resource groupの削除
```
az group delete --name ResourceGroupName
```