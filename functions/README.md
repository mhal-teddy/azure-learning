## 前準備
Azure functionsを使うためにはstorage accountが必要になるので、事前に作っておく。

## Azure Functions Core Tools をインストールする
[公式ドドキュメント](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp#install-the-azure-functions-core-tools)

インストールすると、`func`コマンドが使えるようになる。

## Azure Functions アプリの作成
Azure関数アプリは、Azure上でサーバーレスでコードを実行するためのプラットフォーム。  
関数アプリの名前は、AppName.azurewebsites.net として一意の FQDN を生成できる必要がある。
```
az functionapp create -n <APP_NAME> -g <RESOURCE_GROUP_NAME> -s <STORAGE_ACCOUNT_NAME> -c <LOCATION> --runtime python --runtime-version 3.10 --os-type linux --functions-version 4
```

## Azure Functions プロジェクトの作成
関数プロジェクトとは、Azure Functionsで実行するコードを整理し、管理するための単位。   
まずはpythonの仮想環境を作る。ローカルでAzure Functionsをテストするので、上記で作ったAzure Functionsアプリのバージョンと合わせる。
```
python -m venv .venv
source .venv/bin/activate
```

仮想環境ができたら関数プロジェクトを作る。  
`FOLDER_NAME`はローカルに作成されるフォルダ名(`example`フォルダに例を入れている。)
```
func init <FOLDER_NAME> --python
```
Azure Functionsではトリガーに基づいてコードが実行される。  
そのため、トリガーを設定する必要がある。`FUNCTION_NAME`は分かりやすい名前で問題ない。
```
cd <FOLDER_NAME>
func new -n <FUNCTION_NAME> --template "HTTP trigger"
```
テンプレートの一覧は`func templates list`で取得できる。

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
[az_funcionapp](https://learn.microsoft.com/ja-jp/cli/azure/functionapp?view=azure-cli-latest#az-functionapp-create)
[azure_functions_core_toolsリファレンス](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-core-tools-reference?tabs=v2#func-init)