import json
from flask import Flask, jsonify
from pymongo import MongoClient
from flask import make_response, request, Response, abort
from functools import wraps
#online example, creates server on ip and returns Hello World

#flask
app = Flask(__name__)

#create MongoDB connection
connection = MongoClient('localhost', 27017)
db = connection.ufo

example1 = [
    {
        'id': 1,
        'name': u'Nick',
        'level': u'user'
    },
    {
        'id': 2,
        'name': u'Eric',
        'level': u'scrub'
    },

]

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/secret-page')
@requires_auth
def secret_page():
    return render_template('secret_page.html')

@app.route("/", methods=['GET'])
def get_root():
    return "This is the root directory"

@app.route("/example1", methods =['GET'])
def get_example1():
    return jsonify({'example1': example1})

@app.route("/example1", methods =['POST'])
def create_example1():
    if not request.json or not 'name' in request.json:
        abort(400)
    example = request.get_json()
    example1.append(example)
    return jsonify(example)
    return "Successfully Posted"


if __name__ == "__main__":
    app.run(host = "172.29.33.66", port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
