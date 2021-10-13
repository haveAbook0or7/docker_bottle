import bottle
import routes # routes.py

if __name__ == "__main__":
    bottle.run(host='0.0.0.0', port=5000, debug=True, reloader=True)