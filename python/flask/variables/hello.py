from flask import Flask
from markupsafe import escape

"""
C.f. https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
"""

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)