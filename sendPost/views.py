from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View
import urllib.request
import json
import traceback

#アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        url = 'http://127.0.0.1:8000/account/register/'
        req_header = {
            'Content-Type': 'application/json',
        }

        req_data = json.dumps({
            'userid': request.POST['userid'],
            'username': request.POST['username'],
            'email': request.POST['email'],
            'profile': request.POST['profile'],
            'password': request.POST['password'],
        })

        req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())
                res_json = {
                    'userid': body['userid'],
                    'error_message': 'null',
                }
                print(body['userid'])
        except:
            traceback.print_exc()
            res_json = {
                'error_message': 'error',
            }
            print('NO')
        return render(request, 'sendPost/index.html', {'user_parts' : '特になし'})

    def get(self, request, *args, **kwargs):
        return  render(request, 'sendPost/create.html')

create_account = Create_account.as_view()

#ログイン
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        url = 'http://127.0.0.1:8000/login/'
        req_header = {
            'Content-Type': 'application/json',
        }
        req_data = json.dumps({
            'email': request.POST['email'],
            'password': request.POST['password'],
        })

        req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())
                res_json = {
                    'token': body['token'],
                    'error_message': 'error',
                }
                print(body['token'])
        except:
            traceback.print_exc()
            res_json = {
                'error_message': 'error',
            }
            print('NO')

        ##セッションに保存する項目は検討
        ##トークンは必ず持つが、ユーザーIDも持ちたいなら、ユーザーアカウント情報をgetしないといけない
        ##request.session['session_userid'] = '仮';

        return render(request, 'sendPost/index.html', {'user_parts' : '特になし'})

    def get(self, request, *args, **kwargs):
        return render(request, 'sendPost/login.html')

account_login = Account_login.as_view()

def IndexView(request):
    return render(request, 'sendPost/index.html')



