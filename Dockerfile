FROM python:3.7-rc-slim

COPY flask-bot /app
WORKDIR /app

ENV FLASK_APP=app.py

RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0