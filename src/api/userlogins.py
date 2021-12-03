import bottle
import os
import json
import mysql.connector
import urllib.request
import base64
import io
import datetime
import smtplib
from email.mime.text import MIMEText
from secrets import token_hex
from beaker.middleware import SessionMiddleware

DATABASE_HOST="db"
DATABASE_PORT=3306
DATABASE_USER="db_user"
DATABASE_PASS="pass"
DATABASE_MYDB="db_canvas"
TZ_ASIA_TOKYO=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=9)

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
    except mysql.connector.Error as e:
        message = e.args
    except Exception as e:
        message = e.args

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
    # m = MIMEText("msg")
    # m['Subject'] = "subject"
    # m['From'] = "fromaddr@test.com"
    # m['To'] = "toaddr@test.com"

    # s = smtplib.SMTP(host="mailhog", port=1025)
    # s.sendmail("fromaddr@test.com", "toaddr@test.com", m.as_string())
    # s.close()
    dt1 = TZ_ASIA_TOKYO+datetime.timedelta(hours=6)

    res = dt1.strftime('%Y/%m/%d %H:%M:%S')

    return res

def sign_up_pre(key, payload, createnew=True):
    postjson = json.load(payload)
    res = {"flg": False}
    message = ""
    # まずは既に登録されているものではないかチェック
    try:
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "SELECT id FROM User WHERE email=%(email)s;"
        cur.execute(query, postjson)
        result = cur.fetchall()
        cur.close()
        conn.close()
        if len(result) == 0:
            res["flg"] = True
        # 既に登録ユーザがいたらエラーメッセージを返す。
        message = "" if res["flg"] else "既に登録されているメールアドレスは使えません。"
    except mysql.connector.Error as e:
        message = "エラー(001)。もう一度始めからやり直してください。"
    except Exception as e:
        message = e.args
    finally:
        if res["flg"] == False:
            return json.dumps({
                "message": message,
                "data": res
            }, indent=4)
    # ここから仮登録
    res["flg"] = False
    try:
        postjson["token"] = token_hex(16)
        postjson["deletedate"] = TZ_ASIA_TOKYO+datetime.timedelta(hours=6)
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "INSERT INTO preUser(email, token, deletedate) VALUES(%(email)s,%(token)s,%(deletedate)s);"
        cur.execute(query, postjson)
        conn.commit()
        cur.close()
        conn.close()
        res["flg"] = True
        message = ""
    except mysql.connector.Error as e:
        message = "エラー(002)。もう一度始めからやり直してください。"
    except Exception as e:
        message = e.args[0]
    finally:
        if res["flg"] == False:
            return json.dumps({
                "message": message,
                "data": res
            }, indent=4)
    # メール配信
    res["flg"] = False
    try:
        m = MIMEText(
            f'''こちらのURLから本登録へお進みください。\n
            なお、URLの有効期限は約6時間です。有効期限が過ぎた場合はもう一度仮登録からやり直して下さい。\n
            http://localhost:8080/signup.html?token={postjson["token"]}'''
        )
        m['Subject'] = "仮登録完了及び本登録URL通知"
        m['From'] = "noreply@test.com"
        m['To'] = postjson["email"]
        s = smtplib.SMTP(host="mailhog", port=1025)
        s.sendmail("noreply@test.com", postjson["email"], m.as_string())
        s.close()
        res["flg"] = True
        message = "仮登録完了しました。"
    except SMTPException as e:
        message = "エラー(003)。もう一度始めからやり直してください。"
    except Exception as e:
        message = e
    finally:
        # 完了
        return json.dumps({
            "message": message,
            "data": res
        }, indent=4)

def sign_up(key, payload, createnew=True):
    postjson = json.load(payload)
    if postjson["flg"] == "mounted":
        return check_token(postjson["data"])
    elif postjson["flg"] == "signup":
        return register(postjson["data"])
    else:
        return json.dumps({
            "message": "エラー。もう一度仮登録からやり直してください。",
            "data": {}
        }, indent=4)

def check_token(data):
    postjson = data
    res = {"flg": False}
    message = "URLが正しくありません。もう一度仮登録からやり直してください。"
    try:
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "SELECT email FROM preUser WHERE token=%(token)s;"
        cur.execute(query, postjson)
        result = cur.fetchall()
        cur.close()
        conn.close()
        if len(result) != 0:
            res["flg"] = True
            res["email"] = result[0][0]
            message = "OK"
    except mysql.connector.Error as e:
        message = e.args[0]
    except Exception as e:
        message = e.args[0]
    finally:
        return json.dumps({
            "message": message,
            "data": res
        }, indent=4)

def register(data):
    postjson = data
    res = {"flg": False}
    message = ""
    # まずはIDが既に登録されているものではないかチェック
    try:
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "SELECT * FROM User WHERE id=%(id)s;"
        cur.execute(query, postjson)
        result = cur.fetchall()
        cur.close()
        conn.close()
        if len(result) == 0:
            res["flg"] = True
        message = "" if res["flg"] else "すでに使用されているIDは使えません。"
    except mysql.connector.Error as e:
        message = e.args[0]
    except Exception as e:
        message = e.args[0]
    finally:
        if res["flg"] == False:
            return json.dumps({
                "message": message,
                "data": res
            }, indent=4)
    # ここから登録
    res["flg"] = False
    try:
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "INSERT INTO User(id, pass, email) VALUES(%(id)s, %(pass)s, %(email)s);"
        cur.execute(query, postjson)
        conn.commit()
        cur.close()
        conn.close()
        res["flg"] = True
        message = ""
    except mysql.connector.Error as e:
        message = "エラー(002)。もう一度仮登録からやり直してください。"
    except Exception as e:
        message = e.args[0]
    finally:
        if res["flg"] == False:
            return json.dumps({
                "message": message,
                "data": res
            }, indent=4)
    # ユーザーの設定保存レコードを作る
    res["flg"] = False
    try:
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "INSERT INTO UserConfig(uid) VALUES(%(id)s);"
        cur.execute(query, postjson)
        conn.commit()
        cur.close()
        conn.close()
        res["flg"] = True
        message = ""
    except mysql.connector.Error as e:
        message = "エラー(003)。もう一度仮登録からやり直してください。"
    except Exception as e:
        message = e.args[0]
    finally:
        if res["flg"] == False:
            return json.dumps({
                "message": message,
                "data": res
            }, indent=4)
    # ユーザーのメモ帳保存ファイルを作成
    res["flg"] = False
    memopath = "./static/usermemo/"
    try:
        if not os.path.isdir(memopath+postjson["id"]):
            os.makedirs(memopath+postjson["id"])
            res["flg"] = True
        else:
            message = "エラー(004)。すでに使用されているIDは使えません。"
    except FileExistsError:
        message = "エラー(005)。もう一度仮登録からやり直してください。"
    except Exception as e:
        message = e.args[0]
    finally:
        if res["flg"] == False:
            return json.dumps({
                "message": message,
                "data": res
            }, indent=4)
    res["flg"] = False
    # 仮登録消す
    try:
        conn = mysql.connector.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_MYDB)
        cur = conn.cursor()
        query = "DELETE FROM preUser WHERE email=%(email)s;"
        cur.execute(query, postjson)
        conn.commit()
        cur.close()
        conn.close()
        res["flg"] = True
        message = "本登録完了しました。"
    except mysql.connector.Error as e:
        message = "エラー(006)。もう一度仮登録からやり直してください。"
    except Exception as e:
        message = e.args[0]
    finally:
        return json.dumps({
            "message": message,
            "data": res
        }, indent=4)
