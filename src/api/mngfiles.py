import bottle
import os
import shutil
import json
import mysql.connector
import urllib.request
import base64
import io
from beaker.middleware import SessionMiddleware

def get_path_str(parray):
    restr = ""
    for arr in parray:
        restr += "/" + arr
    return restr

def get_path_arr(pstr):
    return pstr.split("/") if pstr!="" else []

# 今のディレクトリのファイル一覧返す。
def get_nowdir_files(key, payload, createnew=True):
    res = {"flg": None}
    msg = ""
    try:
        # ログイン中のユーザーを取得
        session1 = bottle.request.environ.get('beaker.session')
        user = session1["user"]
        # user = "abcde12345" # テスト用 TODO
        nowdir = ""
        # POSTのデータがあったら取得
        if not payload == None:
            postjson = json.load(payload)
            nowdir = get_path_str(postjson["nowdir"])
        # ゲストユーザーならエラー
        if user == "guest":
            res["user"] = user
            return json.dumps({
                "message": "この機能を利用するにはサインインしてください。",
                "data": res
            }, ensure_ascii=False, indent=4)
        # 今のディレクトリのファイル一覧取得
        res["user"] = user
        res["path"] = get_path_arr(nowdir[1:])
        res["dirlist"] = os.listdir(f'./static/usermemo/{user}{nowdir}')
        res["flg"] = True
    except:
        res["flg"] = False
        msg = "エラーが起きました。\n再読み込みしても直らない場合は一度ウィンドウを閉じて再ログインしてください。"
    return json.dumps({
        "message": msg,
        "data": res
    }, ensure_ascii=False, indent=4)
# セッションに開くファイルを格納する。
def set_open_file(key, payload, createnew=True):
    res = {"flg": None}
    try:
        # ログイン中のユーザーを取得
        session1 = bottle.request.environ.get('beaker.session')
        user = session1["user"]
        # user = "abcde12345" # テスト用 TODO
        # ゲストユーザーならエラー
        if user == "guest":
            return json.dumps({
                "message": "この機能を利用するにはサインインしてください。",
                "data": res
            }, ensure_ascii=False, indent=4)
        # 開くファイルパス取得してセッションに保存
        postjson = json.load(payload)
        session1["openfile"] = user + get_path_str(postjson["openfile"])
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
    res = {"flg": None}
    try:
        # ログイン中のユーザーを取得
        session1 = bottle.request.environ.get('beaker.session')
        user = session1["user"]
        # user = "abcde12345" # テスト用 TODO
        # ゲストユーザーならエラー
        if user == "guest":
            return json.dumps({
                "message": "この機能を利用するにはサインインしてください。",
                "data": res
            }, ensure_ascii=False, indent=4)
        # セッションから開くファイルパス取得
        if "openfile" not in session1:
            session1["openfile"] = None
            session1.save()
        userpath = session1["openfile"]
        # バイナリデータ所得後加工して返す
        if userpath != None:
            img_binary = ""
            with open(f'./static/usermemo/{userpath}', 'rb') as f:
                img_binary = f.read()
            str_img = base64.b64encode(img_binary).decode()
            res["openfile_img"] = f'data:image/png;base64,{str_img}'
            file_neme = userpath.split("/")[len(userpath.split("/"))-1]
            res["openfile_neme"] = file_neme.replace('.png', '')
            res["openfile_path"] = userpath.replace(file_neme, '')
            res["flg"] = True
        else:
            raise Exception
    except:
        res["flg"] = False
    return json.dumps({
        "message": '',
        "data": res
    }, ensure_ascii=False, indent=4)
# 新しいフォルダを作る。
def create_folder(key, payload, createnew=True):
    res = {"flg": None}
    try:
        session1 = bottle.request.environ.get('beaker.session')
        user = session1["user"]
        # user = "abcde12345" # テスト用 TODO
        # ゲストユーザーならエラー
        if user == "guest":
            return json.dumps({
                "message": "この機能を利用するにはサインインしてください。",
                "data": res
            }, ensure_ascii=False, indent=4)
        postjson = json.load(payload)
        # パスとファイル名取得
        save_path = user + get_path_str(postjson["path"])
        save_name = "新しいフォルダ"
        # 既存ディレクトリリスト取得
        dirs = []
        for current_dir, sub_dirs, files_list, in os.walk(f'./static/usermemo/{user}'):
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
        res["flg"] = True
    except:
        res["flg"] = False
    return json.dumps({
        "message": "保存が完了しました。" if res["flg"] else "エラーメッセージ",
        "data": res
    }, ensure_ascii=False, indent=4)
# フォルダやファイルを削除する。
def delete_item(key, payload, createnew=True):
    try:
        session1 = bottle.request.environ.get('beaker.session')
        user = session1["user"]
        # user = "abcde12345" # テスト用 TODO
        # ゲストユーザーならエラー
        if user == "guest":
            return json.dumps({
                "message": "この機能を利用するにはサインインしてください。",
                "data": res
            }, ensure_ascii=False, indent=4)
        # パスとモード取得
        postjson = json.load(payload)
        mode = postjson["mode"]
        delete_path = user + get_path_str(postjson["path"])
        # 削除対象が存在したら削除
        if mode == "file":
            if os.path.isfile(f'./static/usermemo/{delete_path}'):
                os.remove(f'./static/usermemo/{delete_path}')
        elif mode == "folder":
            if os.path.isdir(f'./static/usermemo/{delete_path}'):
                shutil.rmtree(f'./static/usermemo/{delete_path}')
        delete_flg = True
    except:
        delete_flg = False
    return json.dumps({
        "message": "削除が完了しました。" if delete_flg else "エラーメッセージ",
        "data": {"flg": delete_flg}
    }, ensure_ascii=False, indent=4)
# フォルダやファイルの名前変更 TODO
def rename_item(key, payload, createnew=True):
    try:
        session1 = bottle.request.environ.get('beaker.session')
        user = session1["user"]
        # user = "abcde12345" # テスト用 TODO
        # ゲストユーザーならエラー
        if user == "guest":
            return json.dumps({
                "message": "この機能を利用するにはサインインしてください。",
                "data": res
            }, ensure_ascii=False, indent=4)
        # 変更前と変更後のパス取得
        postjson = json.load(payload)
        before_path = user + get_path_str(postjson["before"])
        after_path = user + get_path_str(postjson["after"])
        # 変更対象が存在したら変更
        if os.path.exists(f'./static/usermemo/{before_path}'):
            os.rename(f'./static/usermemo/{before_path}', f'./static/usermemo/{after_path}')
        rename_flg = True
    except:
        rename_flg = False
    return json.dumps({
        "message": "変更が完了しました。" if rename_flg else "エラーメッセージ",
        "data": {"flg": rename_flg}
    }, ensure_ascii=False, indent=4)