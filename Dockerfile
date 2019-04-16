FROM python:3.7-rc-slim

COPY flask-bot /app
WORKDIR /app

ENV FLASK_APP=app.py

EXPOSE 5000

RUN pip install -r requirements.txt

CMD flask run