# 気象データ明細出力_フロントシステム

## システム概要
画面で指定した年・月・地域の気象データを収集し、エクセルファイルとしてダウンロードできるシステムです。

## パッケージ構成(一部省略)

```bash
$ tree
.
├── MdScrapingDjangoWeb #設定ファイル 開発環境ごとのサーバーサイドAPIのURL変更などを行う。
│   
├── Procfile #Herokuサーバー用設定ファイル
├── media
│   └── file #サーバーサイドAPIから受け取るバイナリデータで構築するエクセルファイルの格納場所
│
├── requirements.txt #使用ライブラリバージョン管理(デプロイ用)
├── runtime.txt #Herokuサーバー上で使用するPythonバージョンを管理
├── sendPost
│   ├── templates #HTMLテンプレート
│   ├── urls.py #ルーティング設定
│   └── views.py #画面処理やサーバーサイドAPIとの通信ロジック
│
├── static
│   ├── css #CSSファイルを管理
│   └── js #Javascriptファイルを管理
└── staticfiles #デプロイ時のcollectStatic用ディレクトリ
```
 
## システムURL
http://www.md-data.net/sendPost 

https://tranquil-meadow-43680.herokuapp.com/sendPost  
(SSL認証がされているURLは上記になります。SSL認証URLのみアクセス可能な場合は上記からアクセスをお願いいたします。)

## その他システムの情報
・システムの処理概要  
・オンライン, バッチそれぞれのアーキテクチャ  
・ER図  
・トランザクジョン管理方式  
・インフラ, ネットワーク構成  

上記の情報及びその他本システムの情報については、  
**気象データ明細出力システム_システム設計ドキュメントレポジトリ**を参照してください。
