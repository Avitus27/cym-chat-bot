FROM python:3.7-rc-slim

ADD flask-bot /app
WORKDIR /app

ENV FLASK_APP="flask_bot/app.py"

RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0
