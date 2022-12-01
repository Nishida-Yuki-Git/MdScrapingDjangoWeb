# 気象データ明細出力_フロントシステム

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
https://www.md-data.net/sendPost