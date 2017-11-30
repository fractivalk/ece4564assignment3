import json
from access_token_code import *
from flask import Flask, jsonify
from pymongo import MongoClient
from flask import make_response, request, Response, abort
from functools import wraps
import socket

import requests
import json
import urllib.request

#curl -u eric:sux -X POST http://172.29.87.247:5000/upload/maxresdefault.jpg


#flask
app = Flask(__name__)

#create MongoDB connection
connection = MongoClient('localhost', 27017)
db = connection.ufo

charSht = [
    {
        'name': u'Nick the Nub',
        'level': 999,
		'class': u'Rogue'
    },
    {
        'name': u'Eric the Error',
        'level': 69,
		'class': u'Senior Scrub'
    },
	{
		'name': u'Colin the Conqueror',
		'level': 999,
		'class': u'Warrior'
	},
	{
		'name': u'Wes the Wise',
		'level': 999,
		'class': u'Mage'
	}

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
    for i in requests.get(api_url, params=auth).json():
        if i['filename'] == download_file:
            id = i['id']
    if id == '':
        return 'File \'{}\' not present in remote directory\n'.format(download_file)
    urllib.request.urlretrieve(requests.get('{}/{}'.format(api_url, id) , params=auth).json()['url'], download_file)
    return 'File \'{}\' downloaded successfully\n'.format(download_file)

@app.route("/", methods =['GET'])
@requires_auth
def get_example1():
    return "This is the root directory. Why are you here?"

@app.route("/upload/<upload_file>", methods =['POST'])
@requires_auth    
def create_upload(upload_file):
    # Set up a session
    session = requests.Session()
    session.headers = {'Authorization': 'Bearer %s' % auth['access_token']}

    # Step 1 - tell Canvas you want to upload a file
    payload = {}
    payload['name'] = upload_file
    payload['parent_folder_path'] = '/'
    r = session.post(api_url, data=payload)
    r.raise_for_status()
    r = r.json()

    # Step 2 - upload file
    payload = list(r['upload_params'].items()) # Note this is now a list of tuples
    with open(upload_file, 'rb') as f:
        file_content = f.read()
    payload.append((u'file', file_content)) # Append file at the end of list of tuples
    r = requests.post(r['upload_url'], files=payload)
    r.raise_for_status() 
    r = r.json()
   
    return "File \'{}\' successfully posted\n".format(upload_file)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print(ip)
    app.run(host = str(ip), port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
