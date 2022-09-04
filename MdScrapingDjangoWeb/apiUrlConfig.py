##バックエンドAPIURLの一元管理クラス

class ApiUrlConfig():
    def __init__(self):
        ##ローカル開発環境
        #self.apiUrl = 'http://127.0.0.1:8000'
        ##LAN内サーバー検証(DHCPのため、適宜変更)
        #self.apiUrl = 'http://192.168.2.101:80'
        ##本番環境用
        self.apiUrl = 'http://117.102.204.252:80'

    def getApiUrl(self):
        return self.apiUrl