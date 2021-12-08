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