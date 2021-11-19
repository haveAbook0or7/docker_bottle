import os
import json
import mysql.connector
import urllib.request
import base64
import io

# ユーザーのディレクトリ取得
def get_user_dir(key, payload, createnew=True):
    postjson = json.load(payload)
    user = postjson["user"]
    memopath = "./static/usermemo/"
    restr = ""
    for current_dir, sub_dirs, files_list, in os.walk(memopath+user): 
        now = current_dir[len(memopath):].split("/")
        if(len(sub_dirs) != 0):
            restr += '{"name": "%s", "children": [' %now[len(now)-1]
        else:
            restr += '{"name": "%s"}]},' %now[len(now)-1]
    
    rejson = json.loads(restr[0:len(restr)-1])
    return json.dumps({
        "message": '',
        "data": rejson
    }, ensure_ascii=False, indent=4)

# メモ帳保存
def upfiles(key, payload, createnew=True):
    postjson = json.load(payload)
    mode = postjson["mode"]
    if mode == "save" :
        return save(jsondata=postjson)
    elif mode == "save_new" :
        return save_new(jsondata=postjson)

# 上書き保存
def save(jsondata):
    postjson = jsondata
    # パスとファイル名取得
    save_path = postjson["path"] 
    save_name = postjson["name"]
    # 保存処理
    pngfile = postjson["png"].replace('data:image/png;base64,', '')
    img_binary = base64.b64decode(pngfile)
    save_flg = True
    try:
        with open(f'./static/usermemo/{save_path}{save_name}', 'bw') as f:
            f.write(img_binary)
    except:
        save_flg = False
    
    return json.dumps({
        "message": "保存が完了しました。" if save_flg else "エラーメッセージ",
        "data": {"flg": save_flg}
    },indent=4)

# 新規保存
def save_new(jsondata):
    postjson = jsondata
    # パスとファイル名取得
    save_path = postjson["path"] 
    save_name = postjson["name"]
    # 既存ファイルリスト取得
    files = []
    for current_dir, sub_dirs, files_list, in os.walk(f'./static/usermemo/{save_path.split("/")[0]}'):
        files += files_list
    # 同じファイル名がないか検索
    cnt = 0
    temp_name = save_name
    while True :
        # 照合
        flg = False
        for f in files :
            if temp_name == f :
                flg = True
        # 同じファイルがあったら後ろに数字を振る
        if flg :
            if cnt == 0 : # 最初だけ形式を揃えるために入れる
                temp_name = save_name.split(".")[0]+ "_"+str(cnt)+"." +save_name.split(".")[1]
            cnt += 1
            split_name = temp_name.split(".")
            temp_name = split_name[0][0:len(split_name[0])-1]+str(cnt)+"." +split_name[1]
        else :
            if cnt != 0 : # 最初の名前と同じファイルがあったら上書きする
                save_name = temp_name
            break
    # 保存処理
    pngfile = postjson["png"].replace('data:image/png;base64,', '')
    img_binary = base64.b64decode(pngfile)
    save_flg = True
    try:
        with open(f'./static/usermemo/{save_path}{save_name}', 'bw') as f:
            f.write(img_binary)
    except:
        save_flg = False

    return json.dumps({
        "message": "保存が完了しました。" if save_flg else "エラーメッセージ",
        "data": {"flg": save_flg}
    }, ensure_ascii=False, indent=4)