from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return username + ' profile'

@app.route('/links')
def links():
    url1 = url_for("index")
    url2 = url_for("login")
    url3 = url_for("profile", username="Jean")

    return '<a href="{}">index</a>  <a href="{}">login</a>  <a href="{}">user</a>'.format(url1, url2, url3)
