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
    user = "abcde12345" # テスト用 TODO
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
        user = "abcde12345" # テスト用 TODO
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
        file_neme = userpath.split("/")[len(userpath.split("/"))-1]
        res["openfile_neme"] = file_neme.replace('.png', '')
        res["openfile_path"] = userpath.replace(file_neme, '')
        res["flg"] = True
    except:
        res["flg"] = False
    return json.dumps({
        "message": '',
        "data": res
    }, ensure_ascii=False, indent=4)
# 新しいフォルダを作る。
def create_folder(key, payload, createnew=True):
    try:
        session1 = bottle.request.environ.get('beaker.session')
        # user = session1["user"]
        user = "abcde12345" # テスト用 TODO
        postjson = json.load(payload)
        # パスとファイル名取得
        save_path = user+postjson["path"]
        save_name = "新しいフォルダ"
        # 既存ディレクトリリスト取得
        dirs = []
        for current_dir, sub_dirs, files_list, in os.walk(f'./static/usermemo/{save_path.split("/")[0]}'):
            dirs += sub_dirs
        # 同じディレクトリ名がないか検索
        cnt = 0
        temp_name = save_name
        while True :
            # 照合
            flg = False
            for f in dirs :
                if temp_name == f :
                    flg = True
            # 同じファイルがあったら後ろに数字を振る
            if flg :
                if cnt == 0 : # 最初だけ形式を揃えるために入れる
                    temp_name = save_name+ "_"+str(cnt)
                cnt += 1
                temp_name = temp_name[0:len(temp_name)-1]+str(cnt)
            else :
                if cnt != 0 : # 最初の名前と同じファイルがあったら上書きする
                    save_name = temp_name
                break
        # ディレクトリを作成。
        os.mkdir(f'./static/usermemo/{save_path}/{save_name}')
        save_flg = True
    except:
        save_flg = False
    return json.dumps({
        "message": "保存が完了しました。" if save_flg else "エラーメッセージ",
        "data": {"flg": save_flg}
    }, ensure_ascii=False, indent=4)