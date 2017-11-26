import json
from flask import Flask, jsonify
from pymongo import MongoClient
from flask import make_response

#online example, creates server on ip and returns Hello World

#flask
app = Flask(__name__)

#create MongoDB connection
connection = MongoClient('localhost', 27017)
db = connection.ufo

example1 = [
    {
        "id": 1,
        'name': u'Nick',
        'level': u'user'
    },
    {
        "id": 2,
        'name': u'Eric',
        'level': u'scrub'
    },

]

@app.route("/example1", methods =['GET'])
def get_example1():
    return jsonify({'example1': example1})

@app.route("/example1", methods = ['POST'])
def create_example1():
    example = {
        'id' : example1[-1]['id'] + 1,
        'name': request.json['name'],
        'level': request.json.get('level', "")
    }
    example1.append(example)
    return jsonify({'example': example}), 201


if __name__ == "__main__":
    app.run(host = "192.168.137.182", port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
