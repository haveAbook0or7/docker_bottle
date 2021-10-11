from bottle import route, response, abort, request, get, static_file
from utils import *
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

@route('/py', method=['GET', 'POST'])
def handle_item():
    try:
        response.headers['Content-Type'] = 'text/html'
        if request.method == 'GET':
            return get_items()
        else:
            return create_item(key=request.query.key, payload=request.body)
    except:
        # internal server error
        abort(500)

@route('/<filename:path>')
def send_static(filename):
    """静的ファイルを返す
    """
    return static_file(filename, root='')

@route('/static/css/<filename:path>')
def send_static(filename):
    """静的ファイルを返す
    """
    return static_file(filename, root=f'{STATIC_DIR}/css')

@route('/static/js/<filename:path>')
def send_static(filename):
    """静的ファイルを返す
    """
    return static_file(filename, root=f'{STATIC_DIR}/js')