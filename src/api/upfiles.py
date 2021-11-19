import os
import json
import mysql.connector
import urllib.request
import base64
import io
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

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

def upfiles1(key, payload, createnew=True):
    postjson = json.load(payload)
    pngfile = postjson["png"].replace('data:image/png;base64,', '')
    img_binary = base64.b64decode(pngfile)
    with open('static/img/canvas3.png', 'bw') as f:
        f.write(img_binary)

    return json.dumps({
        "message": 'fff',
        "data": "img_binary"
    },indent=4)

def upfiles2(key, payload, createnew=True):
    postjson = json.load(payload)
    save_path = postjson["path"] 
    save_name = postjson["name"]
    pngfile = postjson["png"].replace('data:image/png;base64,', '')
    img_binary = base64.b64decode(pngfile)
    with open(f'./static/usermemo/{save_path}{save_name}', 'bw') as f:
        f.write(img_binary)

    return json.dumps({
        "message": 'fff',
        "data": "img_binary"
    },indent=4)
