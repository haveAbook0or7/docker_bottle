import bottle
import os
import json
import mysql.connector
import urllib.request
import base64
import io
from beaker.middleware import SessionMiddleware
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def get_login_user():
    # セッションを取得
    session1 = bottle.request.environ.get('beaker.session')
    session1["user"] = "abcde12345"
    if "user" not in session1:
        session1["user"] = "ゲスト"
    session1.save()
    res = {}
    res["user"] = session1["user"]
    return json.dumps({
        "message": None,
        "data": res
    },
    indent=4)
