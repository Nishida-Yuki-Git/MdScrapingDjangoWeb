from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View
import urllib.request
import json
import traceback
from MdScrapingDjangoWeb.apiUrlConfig import ApiUrlConfig
import mimetypes
from django.http import HttpResponse
import shutil
from pathlib import Path
import os


class Create_account(CreateView):
    """ アカウント作成View
    """

    def post(self, request, *args, **kwargs):
        """
        ユーザーアカウント作成を実行する

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト

        Returns
        ----------
        django.shortcuts.render
            HttpResponseオブジェクト
        """

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
        """
        アカウント作成ページの表示

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト

        Returns
        ----------
        django.shortcuts.render
            HttpResponseオブジェクト
        """

        return render(request, 'sendPost/create.html')

create_account = Create_account.as_view()


class Account_login(View):
    """ ログインView
    """

    def post(self, request, *arg, **kwargs):
        """
        ログイン処理を実行する

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト

        Returns
        ----------
        django.shortcuts.render
            HttpResponseオブジェクト
        """

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
        """
        ログインページを表示する

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト

        Returns
        ----------
        django.shortcuts.render
            HttpResponseオブジェクト
        """

        return render(request, 'sendPost/login.html')

account_login = Account_login.as_view()


def indexView(request):
    """
    メインページの初期読み込み

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    django.shortcuts.render
        HttpResponseオブジェクト
    """

    return render(request, 'sendPost/index.html')


def results(request):
    """
    メイン業務実行

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    django.shortcuts.render
        HttpResponseオブジェクト
    """

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


def errorResult(request, result_file_num):
    """
    エラーファイル再作成業務実行

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    result_file_num : str
        ファイル番号

    Returns
    ----------
    django.shortcuts.render
        HttpResponseオブジェクト
    """

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


def download(request, result_file_num):
    """
    ファイルダウンロード実行

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    result_file_num : str
        ファイル番号

    Returns
    ----------
    django.shortcuts.render
        HttpResponseオブジェクト
    """

    host = ApiUrlConfig().getApiUrl()
    url = host+'/md-data/download/' + str(result_file_num) + '/'
    req_header = {
        'Content-Type': 'application/json',
    }

    req_data = json.dumps({})

    byte_data_list = None

    req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            byte_data_list = body['byte_data_list']
    except:
        return render(request, 'sendPost/index.html')

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    FILE_SAVE_DIR = '/file/'
    name = str(result_file_num) + ".xlsx"

    os.chdir(MEDIA_ROOT)
    middle_save_path = MEDIA_ROOT + FILE_SAVE_DIR + str(result_file_num)
    user_file = MEDIA_ROOT + FILE_SAVE_DIR + name

    byte_data = bytes(byte_data_list)
    with open(middle_save_path + ".xlsx", "wb") as f:
        f.write(byte_data)

    response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={name}'

    with open(user_file, "rb") as f:
        shutil.copyfileobj(f, response)

    return response


def setKenList(request):
    """
    県名リスト作成

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    ken_req_list : list
        県名リスト
    """

    ken_req_list = []
    index = 0
    for i in range(50):
        try:
            ken_req_list.append(request.POST['ken-select' + str(index)])
            index += 1
        except:
            break
    return ken_req_list


def setMdList(request):
    """
    気象データ項目リスト作成

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    md_req_list : list
        気象データ項目リスト
    """

    md_req_list = []
    index = 0
    for i in range(5):
        try:
            md_req_list.append(request.POST['md-item-select' + str(index)])
            index += 1
        except:
            break
    return md_req_list

