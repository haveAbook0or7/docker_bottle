import bottle
import os
import json
import mysql.connector
import urllib.request
import base64
import io
from beaker.middleware import SessionMiddleware

# 今のディレクトリのファイル一覧返す。
def get_nowdir_files(key, payload, createnew=True):
    session1 = bottle.request.environ.get('beaker.session')
    # user = session1["user"]
    user = "abcde12345" # テスト用
    nowdir = ""
    if not payload == None:
        postjson = json.load(payload)
        nowdir = postjson["nowdir"]
    res = {"flg": False}
    # ゲストユーザーならエラー
    if user == "guest":
        return json.dumps({
            "message": "この機能を利用するにはサインインしてください。",
            "data": res
        }, ensure_ascii=False, indent=4)
    # 今のディレクトリのファイル一覧取得
    memopath = "./static/usermemo/"
    res["user"] = user
    path = user + nowdir
    res["path"] = path.split('/')
    res["dirlist"] = os.listdir(memopath + path)
    return json.dumps({
        "message": '',
        "data": res
    }, ensure_ascii=False, indent=4)
# セッションに開くファイルを格納する。
def set_open_file(key, payload, createnew=True):
    res = {}
    try:
        postjson = json.load(payload)
        session1 = bottle.request.environ.get('beaker.session')
        # user = session1["user"]
        user = "abcde12345" # テスト用
        session1["openfile"] = f'{user}{postjson["openfile"]}'
        res["user"] = user
        res["flg"] = True
    except:
        res["flg"] = False
    return json.dumps({
        "message": '',
        "data": res
    }, ensure_ascii=False, indent=4)
# 開くファイルを取得する。
def get_open_file():
    res = {}
    try:
        session1 = bottle.request.environ.get('beaker.session')
        memopath = "./static/usermemo/"
        userpath = session1["openfile"]
        img_binary = ""
        with open(f'{memopath}{userpath}', 'rb') as f:
            img_binary = f.read()
        str_img = base64.b64encode(img_binary).decode()
        res["openfile_img"] = f'data:image/png;base64,{str_img}'
        res["openfile_neme"] = userpath.split("/")[len(userpath.split("/"))-1].replace('.png', '')
        res["flg"] = True
    except:
        res["flg"] = False
    return json.dumps({
        "message": '',
        "data": res
    }, ensure_ascii=False, indent=4)