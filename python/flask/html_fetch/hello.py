from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def hello_world():
    return send_from_directory('static', 'foo.html')

@app.route('/hello')
def hello():
    return {'message': 'Hello, World'}