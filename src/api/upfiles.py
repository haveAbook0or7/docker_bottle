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
    #Base64でエンコードする画像のパス
    target_file='static/img/canvas.jpg'
    ff = 'static/img/canvas2.jpg'
    
    with open(target_file, 'rb') as f:
        data = f.read()
    
    #Base64で画像をエンコード
    encode=base64.b64encode(data)
    img_binary = base64.b64decode(encode)
    with open(ff, 'bw') as f:
        f.write(img_binary)

def upfiles1(key, payload, createnew=True):
    postjson = json.load(payload)
    pngfile = postjson["png"].replace('data:image/png;base64,', '')
    img_binary = base64.b64decode(pngfile)
    with open('static/img/canvas3.jpg', 'bw') as f:
        f.write(img_binary)

    return json.dumps({
        "message": 'fff',
        "data": "img_binary"
    },indent=4)