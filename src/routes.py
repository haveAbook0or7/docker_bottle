from bottle import route, response, abort, request, get, static_file
from api.userconfig import *
from api.mngfiles import *
from api.upfiles import *
from api.userlogins import *
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
VIEWS_DIR = os.path.join(BASE_DIR, 'views')
# index.html
@route('/')
def send_static():
    return static_file('index.html', root=f'{VIEWS_DIR}')
# その他のhtml系ファイル
@route('/<filename>')
def send_static(filename):
    return static_file(filename, root=f'{VIEWS_DIR}')
# css, js, imgファイルなど
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}')
# 以下python系設定
@route('/py', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return test_mail()
        else:
            return select(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)
# サインアップ
@route('/userlogins/signup_pre', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return sign_up_pre(key=request.query.key, payload=request.body)
    except:
        abort(500)
@route('/userlogins/signup', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return sign_up(key=request.query.key, payload=request.body)
    except:
        abort(500)
# サインイン
@route('/userlogins/signin', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return sign_in(key=request.query.key, payload=request.body)
    except:
        abort(500)
# サインアウト
@route('/userlogins/signout', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return sign_out()
    except:
        abort(500)
# ログインユーザー取得
@route('/userlogins/getuser', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return get_login_user()
    except:
        # internal server error
        abort(500)

@route('/userconfig/select', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return select()
    except:
        # internal server error
        abort(500)
@route('/userconfig/update', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return update(key=request.query.key, payload=request.body)
        else:
            return get_test()
    except:
        # internal server error
        abort(500)

@route('/upfiles/upload', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return upfiles(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)

@route('/upfiles/getdir', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return get_user_dir()
    except:
        # internal server error
        abort(500)
# 現在のディレクトリ取得
@route('/mngfiles/getnowdir', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return get_nowdir_files(key=None, payload=None)
        else:
            return get_nowdir_files(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)
# ファイルを開くときの処理
@route('/mngfiles/openfile', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return set_open_file(key=request.query.key, payload=request.body)
        else:
            return get_open_file()
    except:
        # internal server error
        abort(500)
# フォルダを作る処理
@route('/mngfiles/createfolder', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return create_folder(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)
# 削除処理
@route('/mngfiles/deleteitem', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return delete_item(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)
# 名前変更処理
@route('/mngfiles/renameitem', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'POST':
            return rename_item(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)