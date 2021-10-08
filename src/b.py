# from bottle import route, run

# @route('/')#今回は一番簡単な奴
# @route('/hi/')#hiでも同じものが出る
# def hibottle():#関数名なんてなんでもよい
#     return "so easy! :)"#ここの文面が出てくる)

# @route('/hi/im/gosu/')
# def imnotgosu():#関数名なんてなんでもよい
#     return "support is so easy dude? :)"#わかるひとにはわかる

# run(host='0.0.0.0', port=5000, debug=True, reloader=True)

# import bottle
# import routes

# if __name__ == "__main__":
#     bottle.run(host='0.0.0.0', port=5000, debug=True, reloader=True)

import json
import mysql.connector
from bottle import route, run


@route('/', methods=['GET'])
def GetZone():
    # return "so easy! :)"#ここの文面が出てくる)
    conn = mysql.connector.connect(host="db", port=3306, user="db_user", password="pass", database="db_hobby")
    cur = conn.cursor()
    query = "SELECT * FROM test;"
    print(query)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return json.dumps(result)

run(host='0.0.0.0', port=5000, debug=True, reloader=True)