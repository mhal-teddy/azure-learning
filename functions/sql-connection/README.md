# Functions と SQL Database の接続
接続には入力バインディング、出力バインディングを用いる。  

## 前準備
[functionsディレクトリ](https://github.com/mhal-teddy/azure-learning/tree/main/functions)に従って、FunctionsアプリとFunctionsプロジェクトを作成する。

また、[sql-databaseディレクトリ](https://github.com/mhal-teddy/azure-learning/tree/main/sql-database)に従って、データベースを作る。

以下の説明では、SQLデータベースのサンプルである`AdventureWorksLT`を使っている。

## データベースの接続文字列
Functionsからデータベースに接続するためには、専用の文字列が必要になる。  
以下のコマンドで取得できる。
```
az sql db show-connection-string -c ado.net -a SqlPassword -s <SERVER_NAME> -n <DATABASE_NAME>
```
認証の種類によって`-a`の値が異なる。詳しくは[az sql dbコマンド](https://learn.microsoft.com/ja-jp/cli/azure/sql/db?view=azure-cli-latest#az-sql-db-show-connection-string)参照。  
取得した文字列に{your_password}などのプレースホルダーがあれば、SQL serverを作ったときの設定に置き換える。

接続文字列を取得したら、Functionsプロジェクトフォルダ内にある`local.settings.json`に下記を追加する。  
<SQL_CONNECTION_STRING>の箇所を接続文字列に置き換える。  
`local.settings.json`はローカルでテストするときに必要になる。
```
# 他の部分は省略
{
  "Values": {
    "SqlConnectionString": <SQL_CONNECTION_STRING>
  }
}
```

## host.json
バイディングの拡張機能をインストールする。  
Functionsプロジェクトの`host.json`を以下のように書き換える。
```
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  },
  "concurrency": {
    "dynamicConcurrencyEnabled": true,
    "snapshotPersistenceEnabled": true
  }
}
```

## プログラムの書き換え
SQL Databaseから入力を受け取ったり、出力したりするためにPythonプログラムを書き換える。  
本ディレクトリの`function_app.py`に例を書いている。  
プログラムの書き方は[入力バインド](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-bindings-azure-sql-input?tabs=isolated-process%2Cnodejs-v4%2Cpython-v2&pivots=programming-language-python)や、[出力バインド](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-bindings-azure-sql-output?tabs=isolated-process%2Cnodejs-v4%2Cpython-v2&pivots=programming-language-python)参照。  
ただし、ドキュメント中にある`function.json`への記入は古いバージョン(v1)の書き方なので使わない。

## ローカルでのテスト
ローカルでテストするときはPCのIPアドレスからデータベースにアクセスするため、ファイアウォールを更新しなければならない。  
`sql-database`ディレクトリにやり方を書いているので参考にすること。

ファイアウォールを更新したら、Functionsプロジェクトに移動して、以下のコマンドでテストできる。
```
pip install -r requirements.txt
func start
```
ターミナルに表示される、`http://localhost:7071/api/<FUNCTION_NAME>`で結果を確かめられる。

本ディレクトリの`function_app.py`の出力は以下のようになる。
```
[{"ProductID": 836, "ModifiedDate": 356.898}, {"ProductID": 822, "ModifiedDate": 356.898}, {"ProductID": 907, "ModifiedDate": 63.9}, {"ProductID": 905, "ModifiedDate": 218.454}, {"ProductID": 983, "ModifiedDate": 461.694}, {"ProductID": 988, "ModifiedDate": 112.998}, {"ProductID": 748, "ModifiedDate": 818.7}, {"ProductID": 990, "ModifiedDate": 323.994}, {"ProductID": 926, "ModifiedDate": 149.874}, {"ProductID": 743, "ModifiedDate": 809.76}]
```

## クラウドでのデプロイ
デプロイするときには、FunctionsからSQL Databaseにアクセスすることになる。  
Azure SQLのファイアウォールに`0.0.0.0`のIPアドレスを設定していない場合は、`sql-database`ディレクトリにしたがって設定する。

次に接続文字列を環境変数に書き込む。
```
az functionapp config appsettings set -n <APP_NAME> -g <RESOURCE_GROUP_NAME> --settings SqlConnectionString=<SQL_CONNECTION_STRING>
```

後は普通のデプロイと同じなので、[functionsディレクトリ](https://github.com/mhal-teddy/azure-learning/tree/main/functions)参照。

## 参考
[Functions to Azure SQL](https://learn.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-azure-sql-vs-code?pivots=programming-language-python)