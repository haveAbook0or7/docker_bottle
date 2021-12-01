import bottle
import os
import json
import mysql.connector
import urllib.request
import base64
import io
import smtplib
from email.mime.text import MIMEText
from beaker.middleware import SessionMiddleware

def get_login_user():
    # セッションを取得
    session1 = bottle.request.environ.get('beaker.session')
    # session1["user"] = "abcde12345"
    if "user" not in session1:
        session1["user"] = "guest"
        session1.save()
    res = {}
    res["user"] = session1["user"]
    return json.dumps({
        "message": None,
        "data": res
    }, indent=4)

def sign_in(key, payload, createnew=True):
    postjson = json.load(payload)
    res = {"flg": False}
    try:
        conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
        cur = conn.cursor()
        query = "SELECT * FROM User WHERE id=%(id)s AND pass=%(pass)s;"
        cur.execute(query, postjson)
        result = cur.fetchall()
        cur.close()
        conn.close()
        if len(result) > 0:
            res["flg"] = True
            res["user"] = result[0][0]
        message = "" if res["flg"] else "ユーザーIDかパスワードが間違っています。"
    except Exception as e:
        message = e

    if res["flg"]:
        session1 = bottle.request.environ.get('beaker.session')
        session1["user"] = res["user"]
        session1.save()

    return json.dumps({
        "message": message,
        "data": res
    }, indent=4)


def sign_out():
    # セッションを取得
    session1 = bottle.request.environ.get('beaker.session')
    session1["user"] = "guest"
    session1.save()
    res = {}
    res["user"] = session1["user"]
    return json.dumps({
        "message": None,
        "data": res
    }, indent=4)

def test_mail():
    m = MIMEText("msg")
    m['Subject'] = "subject"
    m['From'] = "fromaddr@test.com"
    m['To'] = "toaddr@test.com"

    s = smtplib.SMTP(host="mailhog", port=1025)
    s.sendmail("fromaddr@test.com", "toaddr@test.com", m.as_string())
    s.close()

    return "done"

def sign_up_pre():

    return json.dumps({
        "message": None,
        "data": None
    }, indent=4)

# def sign_up():
