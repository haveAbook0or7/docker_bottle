import os
import json
import mysql.connector
import urllib.request

def get_items():
    # with open('template.html', mode='rb') as g:
    #     t = html.fromstring(g.read())
    #     text = t.text_content().strip()
    #     return t
    # fin=open('template.txt')
    #     line=fin.read()
    #     print(line)
    #     fin.close()
    f = open('index.html', 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    return data

    
    # with urllib.request.urlopen('https://codecamp.jp') as f:
    #     return f.read.decode('utf-8')
    # conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_hobby")
    # cur = conn.cursor()
    # query = "SELECT * FROM test;"
    # print(query)
    # cur.execute(query)
    # result = cur.fetchall()
    # cur.close()
    # conn.close()
    # return json.dumps(result, indent=4)
    # return json.dumps(os.listdir("."), indent=4)

def create_item(key, payload, createnew=True):
    message = "updated: {}".format(key)
    if createnew: message = "created: {}".format(key)

    return json.dumps({
        "message": message,
        "payload": json.load(payload)},
        indent=4)