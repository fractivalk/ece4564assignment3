import pymongo
from flask import Flask

#online example, creates server on ip and returns Hello World

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host = "192.168.137.182", port=5000, debug=True) #IP is based of current pi being used, 5000 is Flask DP
