## Azure Functions Core Tools をインストールする
[公式ドドキュメント](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp#install-the-azure-functions-core-tools)

インストールすると、`func`コマンドが使えるようになる。

## Azure Functions にデプロイする環境の作成
関数プロジェクトを作成する。関数プロジェクトとは、特定のトリガーに応答する関数を1つまたは複数含んだコンテナのこと。  
`FOLDER_NAME`はローカルに作成されるフォルダ名(`example`フォルダに例を入れている。)
```
func init <FOLDER_NAME> --python
```
関数をプロジェクトに追加する。`FUNCTION_NAME`は分かりやすい名前で問題ない。
```
cd <FOLDER_NAME>
func new --name <FUNCTION_NAME> --template "HTTP trigger"
```
HTTP triggerの場合、上記のコマンドを実行すると、`Select a number for Auth Level:`という文字列が表示される。  
関数にアクセスするために必要な認可キーを表すので、適切なものを選択する。

## テスト
```
func start
```
コマンドラインに表示されたポート番号にアクセスすると挙動が確かめられる。  
正常に動作すると、以下の文字列がブラウザに表示される。  
なお、クエリパラメータをURLに付加すると、それに応じたレスポンスが返ってくるようになっている。
```
This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.
```

## デプロイのための前準備
デプロイするためには以下の3つが必要となる。
- リソースグループ
- ストレージアカウント
- 関数アプリ：関数プロジェクトを実行するための実行環境

リソースグループとストレージアカウントの作成は、本リポジトリの別ディレクトリ参照。  

### 関数アプリの作成
`APP_NAME`にはグローバルで一意な名前をつける。
```
az functionapp create --resource-group <RESOURCE_GROUP_NAME> --consumption-plan-location <LOCATION_NAME> --runtime python --runtime-version <PYTHON_VERSION> --functions-version 4 --name <APP_NAME> --os-type linux --storage-account <STORAGE_NAME>
```

## デプロイ
ローカルに作った関数プロジェクトのフォルダに移動して、下記コマンドを実行する。
```
func azure functionapp publish <APP_NAME>
```
以下のURLでアクセスすることができる。認可レベルを設定しているときは認可キーが必要になる。
```
https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>?code=<API_KEY>
```
認可キーは以下のコマンドを実行して出力された`default`に書いてある。
```
az functionapp function keys list --function-name <FUNCTION_NAME> -g <RESOURCE_GROUP_NAME> -n <APP_NAME>
```
Azure functionsにリクエストのキーがあるとき(たとえば`example/function_app.py`参照)、URLの最後にクエリパラメータを渡すと、それに応じたレスポンスを得ることができる。

## 関数アプリの一覧表示
```
az functionapp list -g <RESOURCE_GROUP_NAME> -o table
```

## 削除
関数アプリの削除
```
az functionapp delete -n <APP_NAME> -g <RESOURCE_GROUP_NAME>
```

## 参考
[Python関数を追加](https://learn.microsoft.com/ja-jp/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser)