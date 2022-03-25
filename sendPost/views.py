from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View
import urllib.request
import json
import traceback
import shutil
from django.http import HttpResponse
import mimetypes
import glob
from MdScrapingDjangoWeb.apiUrlConfig import ApiUrlConfig

##アカウント作成view
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        host = ApiUrlConfig().getApiUrl()
        url = host+'/account/register/'
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

        res_create_account = {
            'status_code': None,
        }

        req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())
                res_create_account['status_code'] = body['status_code']
                if res_create_account['status_code'] == 1:
                    return render(request, 'sendPost/create.html', {'res_create_account': res_create_account})
        except:
            traceback.print_exc()
            res_create_account['status_code'] = 1
            return render(request, 'sendPost/create.html', {'res_create_account': res_create_account})
        return render(request, 'sendPost/index.html', {'res_create_account': res_create_account})

    def get(self, request, *args, **kwargs):
        return render(request, 'sendPost/create.html')

create_account = Create_account.as_view()


##ログインview
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        #ログイン処理
        host = ApiUrlConfig().getApiUrl()
        url = host+'/login/'
        req_header = {
            'Content-Type': 'application/json',
        }
        req_data = json.dumps({
            'email': request.POST['email'],
            'password': request.POST['password'],
        })

        res_main = {
            'status_code': None,
            'token': None,
            'userid': None,
            'user_input_item_list' : None,
            'user_process_result' : None,
        }

        req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())
                res_main['token'] = body['token']
        except:
            traceback.print_exc()
            res_main['status_code'] = 1
            return render(request, 'sendPost/login.html', {'res_main': res_main})

        #認証チェック(ユーザーIDの取得)
        url = host+'/account/mypage/'
        req_header = {
            'Authorization': 'JWT '+res_main['token'],
        }
        req_data = json.dumps({})

        req = urllib.request.Request(url, data=req_data.encode(), method='GET', headers=req_header)
        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())
                res_main['userid'] = body['userid']
                res_main['status_code'] = body['status_code']
                if res_main['status_code'] == 1:
                    return render(request, 'sendPost/login.html', {'res_main': res_main})
        except:
            traceback.print_exc()
            res_main['status_code'] = 1
            return render(request, 'sendPost/login.html', {'res_main': res_main})

        #メインビジネス初期アクセス
        url = host+'/md-data/init/'
        req_header = {
            'Content-Type': 'application/json',
        }
        req_data = json.dumps({
            'userid': res_main['userid'],
        })

        req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
        try:
            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())
                res_main['user_input_item_list'] = body['user_input_item_list']
                res_main['user_process_result'] = body['user_process_result']
                res_main['status_code'] = body['status_code']
        except:
            traceback.print_exc()
            res_main['status_code'] = 1

        if res_main['status_code'] == 1:
            res_main = None
            res_main = {
                'status_code' : None,
            }
            res_main['status_code'] = 1

        return render(request, 'sendPost/index.html', {'res_main': res_main})

    def get(self, request, *args, **kwargs):
        return render(request, 'sendPost/login.html')

account_login = Account_login.as_view()


##初期読み込み
def indexView(request):
    return render(request, 'sendPost/index.html')


##メイン業務実行
def results(request):
    ##認証チェック
    host = ApiUrlConfig().getApiUrl()
    url = host+'/account/login-check/'
    req_header = {
        'Authorization': 'JWT '+request.POST['token'],
    }
    req_data = json.dumps({})

    res_main = {
        'status_code' : None,
        'user_input_item_list' : None,
        'user_process_result' : None,
        'check_message' : None,
    }

    req = urllib.request.Request(url, data=req_data.encode(), method='GET', headers=req_header)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            res_main['status_code'] = body['status_code']
            if res_main['status_code'] == 1:
                res_main['status_code'] = 3
                return render(request, 'sendPost/index.html', {'res_main': res_main})
    except:
        traceback.print_exc()
        res_main['status_code'] = 3
        return render(request, 'sendPost/index.html', {'res_main': res_main})

    ##メイン業務実行
    url = host+'/md-data/main-logic/'
    req_header = {
        'Content-Type': 'application/json',
    }

    ken_req_list = setKenList(request)
    md_req_list = setMdList(request)
    req_data = json.dumps({
        'userid': request.POST['userid'],
        'start_year': request.POST['start-year-select'],
        'end_year': request.POST['end-year-select'],
        'start_month': request.POST['start-month-select'],
        'end_month': request.POST['end-month-select'],
        'ken': ken_req_list,
        'md_item': md_req_list,
    })

    req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            res_main['user_input_item_list'] = body['user_input_item_list']
            res_main['user_process_result'] = body['user_process_result']
            res_main['status_code'] = body['status_code']
            res_main['check_message'] = body['check_message']
    except:
        traceback.print_exc()
        res_main['status_code'] = 3

    if res_main['status_code'] == 0:
        res_main['status_code'] = 2
    elif res_main['status_code'] == 3:
        res_main = None
        res_main = {
            'status_code' : None,
        }
        res_main['status_code'] = 3

    return render(request, 'sendPost/index.html', {'res_main': res_main})


##エラーファイル再構成
def errorResult(request, result_file_num):
    ##メイン業務実行
    host = ApiUrlConfig().getApiUrl()
    url = host+'/md-data/error-request/'
    req_header = {
        'Content-Type': 'application/json',
    }

    req_data = json.dumps({
        'result_file_num': str(result_file_num),
    })

    res_main = {
        'status_code' : None,
        'user_input_item_list' : None,
        'user_process_result' : None,
    }

    req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            res_main['user_input_item_list'] = body['user_input_item_list']
            res_main['user_process_result'] = body['user_process_result']
            res_main['status_code'] = body['status_code']
    except:
        traceback.print_exc()
        res_main['status_code'] = 3

    if res_main['status_code'] == 0:
        res_main['status_code'] = 2
    elif res_main['status_code'] == 3:
        res_main = None
        res_main = {
            'status_code' : None,
        }
        res_main['status_code'] = 3

    return render(request, 'sendPost/index.html', {'res_main': res_main})


##ファイルダウンロード
def download(request, result_file_num):
    host = ApiUrlConfig().getApiUrl()
    file_dir = '/meteorologicalDataScrapingApp/media/file/'
    file_name = str(result_file_num) + '.xlsx'
    get_file_url = host+file_dir+file_name

    user_file = urllib.request.urlretrieve(get_file_url, file_name)

    response = HttpResponse(content_type=mimetypes.guess_type(file_name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    shutil.copyfileobj(user_file[0], response)

    return response
    '''
    #ログイン処理
    url = 'http://192.168.2.112:80/md-data/download/'
    req_header = {
        'Content-Type': 'application/json',
    }
    req_data = json.dumps({
        'result_file_num': result_file_num,
    })

    req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
    except:
        traceback.print_exc()
        res_main = {
            'status_code': 1,
        }
        return render(request, 'sendPost/index.html', {'res_main': res_main})

    #以下の方式は使用しません(URLをクライアントにスルーするだけにするから)
    file_url = body['file_url']
    #user_file = urllib.request.urlretrieve(file_url, "sample.xlsx")
    user_file = glob.glob(file_url)
    file_name = "fhweifhwif.xlsx"

    response = HttpResponse(content_type=mimetypes.guess_type(file_name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    shutil.copyfileobj(user_file[0], response)

    return response
    '''


##県名リストの作成
def setKenList(request):
    ken_req_list = []
    index = 0
    for i in range(50):
        try:
            ken_req_list.append(request.POST['ken-select' + str(index)])
            index += 1
        except:
            break
    return ken_req_list

##気象項目リストの作成
def setMdList(request):
    md_req_list = []
    index = 0
    for i in range(5):
        try:
            md_req_list.append(request.POST['md-item-select' + str(index)])
            index += 1
        except:
            break
    return md_req_list

