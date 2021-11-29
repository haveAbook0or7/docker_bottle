import bottle
import routes # routes.py
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': './data',
    'session.auto': True
}
app1 = SessionMiddleware(bottle.app(), session_opts)

if __name__ == "__main__":
    bottle.run(app=app1, host='0.0.0.0', port=5000, debug=True, reloader=True)