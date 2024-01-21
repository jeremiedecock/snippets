FROM python:3.8

RUN pip install panel hvplot

# ADD http://archive.ics.uci.edu/ml/machine-learning-databases/00357/occupancy_data.zip /data/
# RUN cd /data/ && unzip occupancy_data.zip

COPY ./app /app/

CMD ["panel", "serve", "--show", "app/paneler.py", "--autoreload", "--address", "0.0.0.0", "--port", "80"]