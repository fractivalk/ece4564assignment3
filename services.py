import json
from flask import Flask, jsonify
from pymongo import MongoClient
from flask import make_response, request, Response, abort
from functools import wraps
import socket

auth = {'access_token':'4511~N31cAx15APjv7QDgwYtY0jIyv7R8bBetGgJFIn0kql3cb4IQjpOyVKPgctxn813C'}
import requests
import json
import urllib.request

#online example, creates server on ip and returns Hello World

#flask
app = Flask(__name__)

#create MongoDB connection
connection = Connection('localhost', 27017)
db = connection.ufo
#connection = MongoClient('localhost', 27017)
#db = connection.ufo

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

    return username == 'eric' and password == 'sux'

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

#Get command handling python http method to download from canvas API at group directory
@app.route("/download/<download_file>", methods=['GET'])
@requires_auth
def get_download(download_file):
    id = ''
    for i in requests.get('https://vt.instructure.com/api/v1/groups/46547/files/', params=auth).json():
        if i['filename'] == download_file:
            id = i['id']
    if id == '':
        return 'File \'{}\' not present in remote directory\n'.format(download_file)
    urllib.request.urlretrieve(requests.get('https://vt.instructure.com/api/v1/groups/46547/files/{}'.format(id) , params=auth).json()['url'], download_file)
    return 'Download successful\n'

@app.route("/", methods =['GET'])
@requires_auth
def get_example1():
    return "This is the root directory. Why are you here?"

@app.route("/upload/<upload_file>", methods =['POST'])
@requires_auth
def create_upload(upload_file):
    #Placeholder: This should send a python http request to the canvas API to upload the specified file to the group directory.
    return "Successfully Posted"


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print(ip)
    app.run(host = str(ip), port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
