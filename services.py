import json
from flask import Flask, jsonify
from pymongo import MongoClient
from flask import make_response, request, abort

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
    app.run(host = "192.168.137.182", port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
