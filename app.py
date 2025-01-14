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

    projects, status = database.get_projects(sort=sort)
    if status == 0:
        for project in projects:
            project['image_link'] = flask.url_for(
                'static', filename=project['image_link'])
        
        html_code = flask.render_template('projects.html',
                                        table=projects)
    else:
        html_code = flask.render_template('projects_error.html',
                                          error=projects)
    
    response = flask.make_response(html_code)
    return response

@app.route('/portfoliodetails', methods=['GET'])
def project_details():
    title = flask.request.args.get('title')
    title = title.replace('-', ' ')
    
    project, status = database.get_projects(title=title)
    try:
        if status == 0:
            if not project or project[0].get('title') != title:
                raise ValueError
            project = project[0]
            project['image_link'] = flask.url_for(
                'static', filename=project['image_link'])
            if project['presentation_link']:
                project['presentation_link'] = flask.url_for(
                    'static', filename=project['presentation_link'])
            if project['writeup_link']:
                project['writeup_link'] = flask.url_for(
                    'static', filename=project['writeup_link'])

            formatted_date = project['date_finished'].strftime("%B %Y")
            html_description = newline_to_paragraphs(
                project['description'])
            dictionaries = []
            if project['other_links']:
                dictionaries = newline_to_dict(project['other_links'])
            
            html_code = flask.render_template(
                'projectdetails.html', title=project['title'],
                date=formatted_date, description=html_description,
                image_link=project['image_link'],
                github=project['github_link'],
                report=project['writeup_link'],
                presentation=project['presentation_link'],
                imagesource_link=project['imagesource_link'],
                imagesource_text=project['imagesource_text'],
                youtube=project['youtube_link'],
                other=dictionaries)
        else:
            html_code = flask.render_template(
                'standard_error.html', title="Project Details Error",
                error=project)
        response = flask.make_response(html_code)
        return response
    except ValueError:
        error_msg = "The project you are looking for does not exist."
        html_code = flask.render_template(
            'standard_error.html', title="Project Not Found",
            error=error_msg)
        response = flask.make_response(html_code)
        return response
    
@app.route('/music', methods=['GET'])
def music():
    html_code = flask.render_template('music.html')
    return flask.make_response(html_code)

@app.route('/getmusic', methods=['GET'])
def get_music():
    sort = flask.request.args.get('music', 'rock')

    if sort == 'rock':
        description = 'The following are a selection of videos of me '
        description += 'playing with the <b>Princeton University Rock '
        description += 'Ensemble</b>.'
        description = newline_to_paragraphs(description)

        videos = [
            "https://www.youtube.com/embed/1YdXFp3KZ18?si=o21N03gHejUyIGjg",
            "https://www.youtube.com/embed/KwN62OBKlFE?si=tRLkvQypzFFM0W2i",
            "https://www.youtube.com/embed/OcQuE6c0Zgg?si=um2qsQZYezrBXlGQ",
            "https://www.youtube.com/embed/BikX3NshRTQ?si=CKDRBpNE5d4iSW10"
        ]

        html_code = flask.render_template('musicdetails.html',
                                          description=description,
                                          videos=videos)
    elif sort == 'theater':
        description = 'The following are a selection of videos of me '
        description += 'playing with the <b>Princeton University '
        description += 'Triangle Club</b> and the <b>LaGuardia High '
        description += 'School Musical</b>.'
        description = newline_to_paragraphs(description)

        videos = [
            "https://www.youtube.com/embed/rjYxdpdKR6o?si=lpqzjo-wNGj63oQg",
            "https://www.youtube.com/embed/hzzsQ9c0vII?si=-tcc4vZYYDVDXtW0",
            "https://www.youtube.com/embed/pvATQqTayxQ?si=G-U3tzn6FACEzs-j"
        ]

        html_code = flask.render_template('musicdetails.html',
                                          description=description,
                                          videos=videos)
    elif sort == 'orchestra':
        description = 'The following are a selection of videos of me '
        description += 'playing with the <b>Princeton University '
        description += 'Orchestra</b> and the <b>LaGuardia High School '
        description += 'Senior Orchestra</b>.'

        videos = [
            "https://www.youtube.com/embed/25lz4yEM5qI?si=swHA5ka0RxsWmsDq",
            "https://www.youtube.com/embed/0dQnPEUe-yk?si=sRmXPFa3F3tcKeUP",
            "https://www.youtube.com/embed/Vq5gA0QSmDs?si=qYJL7lZKclgjK4oX",
            "https://www.youtube.com/embed/JxremZRzzMg?si=bUh3iNPUrAXbVSXk"
        ]

        html_code = flask.render_template('musicdetails.html',
                                          description=description,
                                          videos=videos)
    elif sort == 'songs':
        description = 'The following is a selection of my '
        description += '<b>songwriting</b>. I\'m currently working on an '
        description += 'EP. Stay Tuned!'

        videos = [
            "https://www.youtube.com/embed/SUbphqbrKaY?si=XMgNgGmALRpO7lph",
            "https://www.youtube.com/embed/65fL-G7TNjQ?si=Blo_-FIJ1bhvtXRF",
            "https://www.youtube.com/embed/eoxE2D0mSrQ?si=hfwXh2W_IyLSsNx1"
        ]

        html_code = flask.render_template('musicdetails.html',
                                          description=description,
                                          videos=videos)

    else:
        error_msg = "A server error occured. Please contact the system "
        error_msg += "administrator."

        html_code = flask.render_template('projects_error.html',
                                          error=error_msg)
    
    response = flask.make_response(html_code)
    return response


@app.route('/about', methods=['GET'])
def about():
    html_code = flask.render_template('about.html')
    return flask.make_response(html_code)

# -----------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    error_msg = "The page you are looking for does not exist."
    html_code = flask.render_template('standard_error.html',
                                      title="Page Not Found",
                                      error=error_msg)
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