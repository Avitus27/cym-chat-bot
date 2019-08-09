import os
import sys
import json
from datetime import datetime
from pymessenger.bot import Bot
import requests
from flask import Flask, request

app = Flask(__name__)
bot = None


@app.route('/', methods=['GET'])
def verify():
    """Verify that the token received is correct.

    When the endpoint is registered as a webhook, it must echo back
    the`hub.challengs` value it receives in the query arguments

    Decorators:
        app.route

    Returns:
        HTTP Response -- 200 OK when no expected args provided or the challenge
                         is correct, 403 when token mismatch
    """
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get(
            "hub.challenge"):
        if not request.args.get(
                "hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "ok", 200


@app.route('/', methods=['POST'])
def webhook():
    """Endpoint for processing incoming messaging events.

    Processes incoming messages

    Decorators:
        app.route
    """
    data = request.get_json()
    log(data)
    # you may not want to log every incoming message in production
    # but it's good for testing

    if data and data.get('object') and data.get('object') == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    # the recipient's ID, which should be your page's facebook
                    # ID
                    recipient_id = messaging_event["recipient"]["id"]
                    # the message's text
                    message_text = messaging_event["message"]["text"]
                    send_message(sender_id, "gwan the lads!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get(
                        "postback"):
                        # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        headers=headers,
        data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = str(msg).format(*args, **kwargs)
        print("{}: {}".format(datetime.now(), msg), file=sys.stderr)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


@app.before_first_request
def set_environment_variables():
    """Set the environment variables.

    Reads the verify and access tokens from the secret.json file

    Decorators:
        app.before_first_request
    """
    try:
        with open("secret.json") as fp:
            config = json.load(fp)
        os.environ["VERIFY_TOKEN"] = config["verify_token"]
        os.environ["ACCESS_TOKEN"] = config["access_token"]
        log("Config loaded access:{} verify:{}".format(
            os.environ['ACCESS_TOKEN'],
            os.environ['VERIFY_TOKEN']))
    except FileNotFoundError as err:
        log("secret.json not found. Is it in the right directory, with app.py?"
            "Setting verify and access to blank")
        os.environ["VERIFY_TOKEN"] = ""
        os.environ["ACCESS_TOKEN"] = ""
    bot = Bot(os.environ["ACCESS_TOKEN"])
