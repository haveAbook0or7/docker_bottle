import os
import json
import mysql.connector
import urllib.request

def get_items():
    # return json.dumps(os.listdir("./static/html"), indent=4)
    conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
    cur = conn.cursor()
    query = "SELECT * FROM test;"
    print(query)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return json.dumps(result, indent=4)

def create_item(key, payload, createnew=True):
    message = "updated:"
    postjson = json.load(payload)

    conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_canvas")
    cur = conn.cursor()
    query = f"SELECT * FROM UserConfig WHERE {postjson['id']};"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()

    res = {}
    res['palette'] = {'black': "#000000", 'one': result[0][1], 'two': result[0][2], 'three': result[0][3], 'four': result[0][4], 'five': result[0][5]}
    res['size'] = {'marker': result[0][6], 'thinPen': result[0][7], 'thickPen': result[0][8], 'eraser': result[0][9]}
    res['alpha'] = {'marker': result[0][10], 'thinPen': result[0][11], 'thickPen': result[0][12], 'eraser': result[0][13]}

    return json.dumps({
        "message": message,
        "data": res
    },
    indent=4)