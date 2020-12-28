from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<a href="{}">foo<a>'.format(url_for('static', filename='foo.html'))

