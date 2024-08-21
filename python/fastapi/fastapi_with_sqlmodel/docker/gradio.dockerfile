FROM python:3.8

RUN pip install gradio

COPY ./app /app/

CMD ["gradio", "app/gradiohello.py"]