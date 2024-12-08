# !/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# Author: Louis Larsen
# -----------------------------------------------------------------------

# Includes serveral essential functions for managing the backend database

# -----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
import dotenv

# -----------------------------------------------------------------------
# Load environment variables
dotenv.load_dotenv()

# Fetch the database URL from the environment and update the prefix
_DATABASE_URL = os.environ.get('DATABASE_URL')
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

# -----------------------------------------------------------------------

# Define the base class
Base = sqlalchemy.orm.declarative_base()

# Define a model class for the 'projects' table
class Project(Base):
    __tablename__ = 'projects'
    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)                 # Primary key column for project title
    description = sqlalchemy.Column(sqlalchemy.String)                             # Column for project description
    date_finished = sqlalchemy.Column(sqlalchemy.Date)                             # Column for project completion date
    image_link = sqlalchemy.Column(sqlalchemy.String)                              # Column for image URL related to the project
    imagesource_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)         # Column for image source text related to the project (Make Optional)
    imagesource_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)         # Column for image source link related to the project (Make Optional)
    youtube_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)             # Column for youtube video related to the project (Make Optional)
    presentation_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)        # Column for presentation related to the project (Make Optional)
    writeup_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)             # Column for writeup related to the project (Make Optional)
    github_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)              # Column for github link related to the project (Make Optional)
    other_links = sqlalchemy.Column(sqlalchemy.String, nullable=True)              # Column for any other links related to the project (Make Optional)

# Create a database engine
_engine = sqlalchemy.create_engine(_DATABASE_URL)

# -----------------------------------------------------------------------

# Function to create the projects table in the database
def create_project_table():
    Base.metadata.create_all(_engine)
    print("database.py: Projects table created successfully.")

# Function to add a new project to the database
def add_project(
        title, description, date_finished, image_link, imagesource_text,
        imagesource_link, youtube_link, presentation_link, writeup_link,
        github_link, other_links):
    
    new_project = Project(
        title=title,
        description=description,
        date_finished=date_finished,
        image_link=image_link,
        imagesource_text=imagesource_text,
        imagesource_link=imagesource_link,
        youtube_link=youtube_link,
        presentation_link=presentation_link,
        writeup_link=writeup_link,
        github_link=github_link,
        other_links=other_links
    )

    with sqlalchemy.orm.Session(_engine) as session:
        session.add(new_project)
        session.commit()
    print("database.py: Project added successfully.")

# Function to remove a project from the database
def remove_project(title):

    with sqlalchemy.orm.Session(_engine) as session:
        # Find the project by title and delete it
        project_to_remove = session.query(Project).filter(
            Project.title.ilike(title+'%')
        ).first()

        if project_to_remove:
            session.delete(project_to_remove)
            session.commit()
            print("database.py: Project removed successfully.")
        else:
            print("database.py: Project could not be found")

# Function to clear all entries from the projects table
def clear_project_table():
    with sqlalchemy.orm.Session(_engine) as session:
        session.query(Project).delete()
        session.commit()
    print("database.py: All projects cleared from the table")

# Function to retrieve projects by title from the database
def get_projects(title='', sort='recent'):
    projects = []

    with sqlalchemy.orm.Session(_engine) as session:
        # Query for projects whose title matches the given string
        if sort == 'recent':
            query = session.query(Project).filter(
                Project.title.ilike(title+'%')
            ).order_by(Project.date_finished.desc())
        elif sort == 'alpha':
            query = session.query(Project).filter(
                Project.title.ilike(title+'%')
            ).order_by(Project.title)
        
        # Iterate over query results to build a list of project dictionaries
        table = query.all()
        for row in table:
            project = {
                'title': row.title,
                'description': row.description,
                'date_finished': row.date_finished,
                'image_link': row.image_link,
                'imagesource_text': row.imagesource_text,
                'imagesource_link': row.imagesource_link,
                'youtube_link': row.youtube_link,
                'presentation_link': row.presentation_link,
                'writeup_link': row.writeup_link,
                'github_link': row.github_link,
                'other_links': row.other_links
            }
            projects.append(project)

    return projects

# -----------------------------------------------------------------------
