# !/usr/bin/env python

# -----------------------------------------------------------------------
# app.py
# Author: Louis Larsen
# -----------------------------------------------------------------------

# The Portfolio Website

# -----------------------------------------------------------------------

import sys
import flask
import database
import json
import html

# -----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='./templates/')

# -----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def start():
    html_code = flask.render_template('starter.html')
    return flask.make_response(html_code)

# -----------------------------------------------------------------------
