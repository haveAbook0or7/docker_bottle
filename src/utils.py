import os
import json
import mysql.connector
import urllib.request

def get_items():
    # return json.dumps(os.listdir("./static/html"), indent=4)
    conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_hobby")
    cur = conn.cursor()
    query = "SELECT * FROM test;"
    print(query)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return json.dumps(result, indent=4)

def create_item(key, payload, createnew=True):
    message = "updated: {}".format(key)
    if createnew: message = "created: {}".format(key)

    return json.dumps({
        "message": message,
        "payload": json.load(payload)},
        indent=4)