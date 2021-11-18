import os
import json
import mysql.connector
import urllib.request
import base64
import io
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def upfiles2(user="abcde12345"):
    memopath = "./static/usermemo/"
    rejson = {"name": user, "children": []}
    restr = ""
    c = ""
    cnt = 1
    for current_dir, sub_dirs, files_list, in os.walk(memopath+user): 
        now = current_dir[len(memopath):].split("/")
        if(len(sub_dirs) != 0):
            cnt+=1
            restr += '{"name": "%s", "children": [' %now[len(now)-1]
        else:
            cnt-=1
            restr += '{"name": "%s"}]},' %now[len(now)-1]
        c += u"now {}   <br>".format(now[len(now)-1])
        c += u"sub {}   <br>".format(sub_dirs)
        c += u"file {}   <br>".format(files_list)
        c += u"cnt {}   <br>".format(cnt)
        c += u"json {}   <br>".format(restr)
        c += "//////////////////////////////////////////////<br>"

        # for subdir in sub_dirs
        #     rejson["children"] += 
    # a = json.dumps(os.walk(f"./static/usermemo/{user}"), indent=4)
    # b = json.loads(a)
    return c

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
