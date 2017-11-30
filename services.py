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
db = connection['ECE4564_Assignment_3']
collection = db['service_auth']
collection.drop()
for item in auth_list:
	db.service_auth.insert_one(item)


charSht = [
	{
		'name': u'Nick_the_Nub',
		'level': 999,
		'class': u'Rogue'
	},
	{
		'name': u'Eric_the_Error',
		'level': 1337,
		'class': u'Senior Scrub'
	},
	{
		'name': u'Colin_the_Conqueror',
		'level': 999,
		'class': u'Warrior'
	},
	{
		'name': u'Wes_the_Wise',
		'level': 999,
		'class': u'Mage'
	}

]

def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""

	return True if db.service_auth.find({"username":username}, {"password":password}).count() > 0 else False


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

@app.route("/", methods =['GET'])
@requires_auth
def get_example1():
	return "This is the root directory. Why are you here?"

@app.route("/Canvas", methods=['GET', 'POST'])
@requires_auth
def canvas():
	if request.method == 'POST':
		file = request.form.get('file')
		operation = request.form.get('operation')
	elif request.method == 'GET':
		file = request.args.get('file')
		operation = request.args.get('operation')

	if operation == 'upload':
		# Set up a session
		session = requests.Session()
		session.headers = {'Authorization': 'Bearer %s' % auth['access_token']}

		# Step 1 - tell Canvas you want to upload a file
		payload = {}
		payload['name'] = file
		payload['parent_folder_path'] = '/'
		r = session.post(api_url, data=payload)
		r.raise_for_status()
		r = r.json()

		# Step 2 - upload file
		payload = list(r['upload_params'].items()) # Note this is now a list of tuples
		with open(file, 'rb') as f:
			file_content = f.read()
		payload.append((u'file', file_content)) # Append file at the end of list of tuples
		r = requests.post(r['upload_url'], files=payload)
		r.raise_for_status()
		r = r.json()
		return "File \'{}\' successfully posted\n".format(file)

	elif operation == 'download':
		id = ''
		for i in requests.get(api_url, params=auth).json():
			if i['filename'] == file:
				id = i['id']
		if id == '':
			return 'File \'{}\' not present in remote directory\n'.format(file)
		urllib.request.urlretrieve(requests.get('{}/{}'.format(api_url, id) , params=auth).json()['url'], file)
		return 'File \'{}\' downloaded successfully\n'.format(file)

'''
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
'''

#custom API functionality

#Get 1

@app.route("/PartyInfo", methods=['GET'])
@requires_auth
def fetch_party_info():
	return jsonify(charSht)

#Get 2

@app.route('/PartyInfo/<char_name>', methods=['GET'])
@requires_auth
def get_char(char_name):
	char = [char for char in charSht if char['name'] == char_name]
	if len(char) == 0:
		abort(404)
	return jsonify({'char': char[0]})

#Post 1

@app.route("/PartyInfo/AddCharacter", methods=['POST'])
@requires_auth
def add_char():
	print(request.json)
	char = {
		'name': request.json['name'],
		'level': request.json['level'],
		'class': request.json['class']
	}
	charSht.append(char)
	#return jsonify({'char': char}), 201

#Post 2

@app.route("/PartyInfo/<char_name>/AddSkill", methods=['POST'])
@requires_auth
def add_skill(char_name):
	'''
	[char for char in charSht if char['name'] == char_name]['Skill'] = request.data
	char = [char for char in charSht if char['name'] == char_name]
	if len(char) == 0:
		abort(404)
	return jsonify({'char': char[0]})
	'''

ledip = ""
""" Listing services available """
myName =  ""
class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)

        myName = name
        if str(name) == 'COLINSLED._http._tcp.local.':
            ip = info.address
            path= ""
            prStr = socket.inet_ntoa(ip)
            #print('Found: ' + str(prStr) + " port: " + str(info.port) + str(info.properties))
            if info.properties:
                print(" Properties Are")
                for key, value in info.properties.items():
                    print (key.decode('UTF-8'))
                    if key.decode("UTF-8") == "path":
                        print ("HI")
                        path = str(value)

            print('http://' + prStr + ":" + str(info.port) + path)

@requires_auth
@app.route("/LED", methods=['GET'])
def led():
    ledstatus = request.args.get('status')
    ledcolor = request.args.get('color')
    ledintensity = request.args.get('intensity')

	# zeroconf = Zeroconf()
	# listener = MyListener()
	# browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    # print(len(request.args))

    # r = requests.get('')
    #
    # r = requests.post('', data={'color':ledcolor, 'status':ledstatus, 'intensity':ledintensity})

    return str(len(request.args)) + ' ' + ledstatus + ' ' + ledcolor + ' ' + str(ledintensity) + '\n'


if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	print(ip)
	app.run(host = str(ip), port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
