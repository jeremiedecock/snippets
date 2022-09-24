#FROM python as wsgi
FROM python

WORKDIR /app
COPY . ./

# C.f. https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/#running
RUN pip install Flask \
 && pip install gunicorn

RUN  pip install .

CMD gunicorn --bind 0.0.0.0:8000 -w 2 'hello:app'