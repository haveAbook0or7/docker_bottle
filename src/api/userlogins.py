import bottle
import os
import json
import mysql.connector
import urllib.request
import base64
import io
from beaker.middleware import SessionMiddleware

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
    }, indent=4)

def sign_in(key, payload, createnew=True):
    postjson = json.load(payload)
    res = {}
    try:
        conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
        cur = conn.cursor()
        query = "SELECT * FROM User WHERE id LIKE %(id)s AND pass LIKE %(pass)s;"
        cur.execute(query, postjson)
        result = cur.fetchall()
        cur.close()
        conn.close()

        res = result
        message = "OK"
    except Exception as e:
        message = e
    
    return json.dumps({
        "message": message,
        "data": res
    }, indent=4)


def sign_out():
    # セッションを取得
    session1 = bottle.request.environ.get('beaker.session')
    session1["user"] = "ゲスト"
    session1.save()
    res = {}
    res["user"] = session1["user"]
    return json.dumps({
        "message": None,
        "data": res
    }, indent=4)

# def sign_up_pre():

# def sign_up():
