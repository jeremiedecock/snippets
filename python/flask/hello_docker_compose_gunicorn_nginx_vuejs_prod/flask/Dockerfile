FROM python:alpine

WORKDIR /app
COPY . ./

# C.f. https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/#running
RUN pip install Flask \
 && pip install Werkzeug \
 && pip install flask-cors \
 && pip install gunicorn

RUN  pip install .

CMD gunicorn -w 2 'hello:app'