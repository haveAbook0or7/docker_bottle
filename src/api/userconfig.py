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
# ペン設定引き出しTODOセッション使う
def select():
    session1 = bottle.request.environ.get('beaker.session')
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
# ペン設定変更 TODO 未完成
def update(key, payload, createnew=True):
    message = ""
    res = {}
    postjson = json.load(payload)

    try:
        conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
        cur = conn.cursor()
        query = """
            UPDATE UserConfig 
            SET color1=%(one)s, color2=%(two)s, color3=%(three)s, color4=%(four)s, color5=%(five)s, 
            marker_size=%()s, thinPen_size=%()s, thickPen_size=%()s, eraser_size=%()s, 
            marker_alpha=%()s, thinPen_alpha=%()s, thickPen_alpha=%()s, eraser_alpha=%()s 
            WHERE uid=%(id)s;
        """
        cur.execute(query, postjson)
        result = cur.fetchall()
        cur.close()
        conn.close()

        message = "OK"
    except Exception as e:
        message = e;

    return json.dumps({
        "message": message,
        "data": res
    },
    indent=4)