# !/usr/bin/env python

# -----------------------------------------------------------------------
# app.py
# Author: Louis Larsen
# -----------------------------------------------------------------------

# The Portfolio Website

# -----------------------------------------------------------------------

import os
import sys
import json
import flask
import flask_mail
import dotenv
import database

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
             "message": "Email sent successfully."}
             ), 200

    except Exception as ex:
        print("app.py: " + str(ex), file=sys.stderr)
        return flask.jsonify(
            {"status": "error", 
             "message": "Failed to send email. Please Try Again Later."}
             ), 500
    
@app.route('/portfolio', methods=['GET'])
def portfolio():
    html_code = flask.render_template('portfolio.html')
    return flask.make_response(html_code)

@app.route('/getprojects', methods=['GET'])
def get_projects():
    sort = flask.request.args.get('sort', 'recent')

    projects = database.get_projects(sort=sort)
    for project in projects:
        project['image_link'] = flask.url_for(
            'static', filename=project['image_link'])
    
    html_code = flask.render_template('projects.html',
                                      table=projects)
    response = flask.make_response(html_code)

    return response

@app.route('/portfoliodetails', methods=['GET'])
def project_details():
    title = flask.request.args.get('title')
    title = title.replace('-', ' ')
    
    project = database.get_projects(title=title)[0]
    project['image_link'] = flask.url_for(
        'static', filename=project['image_link'])
    if project['presentation_link']:
        project['presentation_link'] = flask.url_for(
            'static', filename=project['presentation_link'])
    if project['writeup_link']:
        project['writeup_link'] = flask.url_for(
            'static', filename=project['writeup_link'])

    formatted_date = project['date_finished'].strftime("%B %Y")
    html_description = newline_to_paragraphs(project['description'])
    dictionaries = []
    if project['other_links']:
        dictionaries = newline_to_dict(project['other_links'])
    
    html_code = flask.render_template('projectdetails.html',
                                      title=project['title'],
                                      date=formatted_date,
                                      description=html_description,
                                      image_link=project['image_link'],
                                      github=project['github_link'],
                                      report=project['writeup_link'],
                                      presentation=project['presentation_link'],
                                      imagesource_link=project[
                                          'imagesource_link'],
                                      imagesource_text=project[
                                          'imagesource_text'],
                                      youtube=project['youtube_link'],
                                      other=dictionaries)
    response = flask.make_response(html_code)

    return response

# -----------------------------------------------------------------------

def newline_to_paragraphs(text):
    lines = text.split('\n')
    html = ''
    for line in lines:
        line = line.strip()
        if line == '<hr>':
            html += '<hr>'
        elif line:
            html += f'<p class="body4">{line}</p>'
    return html

def newline_to_dict(text):
    lines = text.split('\n')
    dictionaries = []
    for line in lines:
        line = line.strip()
        dictionary = json.loads(line)
        dictionaries.append(dictionary)
    return dictionaries