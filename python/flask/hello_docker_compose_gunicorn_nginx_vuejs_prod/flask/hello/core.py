from flask import Flask
from flask_cors import cross_origin

# C.f. https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# C.f. https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route("/")
@cross_origin(origins=['http://127.0.0.1'])
def hello_world():
    return {"message": "Hello from Flask!"}
