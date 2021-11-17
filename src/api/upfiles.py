import os
import json
import mysql.connector
import urllib.request
import base64
import io
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def upfiles2(user="abcde12345"):
    a = json.dumps(os.listdir(f"./static/usermemo/"), indent=4)
    b = json.loads(a)
    return str(len(b))

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