# -*- coding: utf-8 -*-
# import bottle

# app = bottle.app()

# @app.route('/hello')
# def index():
#     return "Hello, World! This is bottle"

# if __name__ == '__main__':
#     app.run(debug=True, reloader=True, host='0.0.0.0', port=5000)

from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host='0.0.0.0', port=5000, debug=True, reloader=True)