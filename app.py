# !/usr/bin/env python

# -----------------------------------------------------------------------
# app.py
# Author: Louis Larsen
# -----------------------------------------------------------------------

# The Portfolio Website

# -----------------------------------------------------------------------

import os
import sys
import flask
import flask_mail
import dotenv
import database
import json
import html

# -----------------------------------------------------------------------

# Create the app
app = flask.Flask(__name__, template_folder='./templates/')

# Set up mail feature
# Load and set environment variables
dotenv.load_dotenv()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

print(os.environ.get('MAIL_USERNAME'))

mail = flask_mail.Mail(app)

# -----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def start():
    html_code = flask.render_template('index.html')
    return flask.make_response(html_code)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = flask.request.json

    # validate input
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return flask.jsonify(
            {"status": "error", 
             "message": "All fields are required"}
             ), 400
    
    try:
        # create message
        msg = flask_mail.Message(
            subject=f"Portfolio Contact from {name}",
            recipients=["lalarsen@alumni.princeton.edu"],
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)

        return flask.jsonify(
            {"status": "success", 
             "message": "Email sent Successfully"}
             ), 200

    except Exception as ex:
        print("app.py: " + str(ex), file=sys.stderr)
        return flask.jsonify(
            {"status": "error", 
             "message": "Failed to send email"}
             ), 500

# -----------------------------------------------------------------------
