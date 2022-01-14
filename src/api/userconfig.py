import bottle
import os
import json
import mysql.connector
import urllib.request
from beaker.middleware import SessionMiddleware

def get_test():
    conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
    cur = conn.cursor()
    query = "SELECT * FROM test;"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return json.dumps(result, indent=4)
# ペン設定引き出し
def select():
    session1 = bottle.request.environ.get('beaker.session')
    if "user" not in session1:
        session1["user"] = "guest"
        session1.save()
    logid = {"id": session1["user"]}
    message = ""
    res = {}
    try:
        conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
        cur = conn.cursor()
        query = "SELECT * FROM UserConfig WHERE uid=%(id)s;"
        cur.execute(query, logid)
        result = cur.fetchall()
        cur.close()
        conn.close()

        res['palette'] = {'black': "#000000", 'one': result[0][1], 'two': result[0][2], 'three': result[0][3], 'four': result[0][4], 'five': result[0][5]}
        res['size'] = {'marker': result[0][6], 'thinPen': result[0][7], 'thickPen': result[0][8], 'eraser': result[0][9]}
        res['alpha'] = {'marker': result[0][10], 'thinPen': result[0][11], 'thickPen': result[0][12], 'eraser': result[0][13]}
        message = "OK"
    except Exception as e:
        message = e

    return json.dumps({
        "message": message,
        "data": res
    },
    indent=4)
# ペン設定変更
def update(key, payload, createnew=True):
    message = ""
    res = {}
    try:
        session1 = bottle.request.environ.get('beaker.session')
        if "user" not in session1:
            session1["user"] = "guest"
            session1.save()
        if session1["user"] == "guest":
            raise Exception(session1["user"])

        postjson = json.load(payload)
        postjson["id"] = session1["user"]
        conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
        conn.autocommit = False
        cur = conn.cursor()
        try:
            query = """
                UPDATE UserConfig 
                SET color1=%(one)s, color2=%(two)s, color3=%(three)s, color4=%(four)s, color5=%(five)s, 
                marker_size=%(markerS)s, thinPen_size=%(thinPenS)s, thickPen_size=%(thickPenS)s, eraser_size=%(eraserS)s, 
                marker_alpha=%(markerA)s, thinPen_alpha=%(thinPenA)s, thickPen_alpha=%(thickPenA)s, eraser_alpha=%(eraserA)s 
                WHERE uid=%(id)s;
            """
            cur.execute(query, postjson)
            conn.commit()
            message = "OK"
        except Exception as e:
            conn.rollback()
            raise
        cur.close()
        conn.close()
    except Exception as e:
        message = str(e)
    finally:
        return json.dumps({
            "message": message,
            "data": res
        },
        indent=4)