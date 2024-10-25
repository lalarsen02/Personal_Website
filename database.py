# !/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# Author: Louis Larsen
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
    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)  # Primary key column for project title
    description = sqlalchemy.Column(sqlalchemy.String)              # Column for project description
    date_finished = sqlalchemy.Column(sqlalchemy.String)            # Column for project completion date
    image_link = sqlalchemy.Column(sqlalchemy.String)               # Column for image URL related to the project
    github_link = sqlalchemy.Column(sqlalchemy.String)              # Column for project's GitHub link

# Create a database engine
_engine = sqlalchemy.create_engine(_DATABASE_URL)

# -----------------------------------------------------------------------

# Function to create the projects table in the database
def create_project_table():
    Base.metadata.create_all(_engine)
    print("Projects table created successfully.")

# Function to add a new project to the database
def add_project(new_project):
    with sqlalchemy.orm.Session(_engine) as session:
        session.add(new_project)
        session.commit()
    print("Project added successfully.")

# Function to clear all entries from the projects table
def clear_project_table():
    with sqlalchemy.orm.Session(_engine) as session:
        session.query(Project).delete()
        session.commit()
    print("All projects cleared from the table")

# Function to retrieve projects by title from the database
def get_projects(title):
    projects = []

    with sqlalchemy.orm.Session(_engine) as session:
        # Query for projects whose title matches the given string
        query = session.query(Project).filter(
            Project.title.ilike(title+'%')
        )
        
        # Iterate over query results to build a list of project dictionaries
        table = query.all()
        for row in table:
            project = {
                'title': row.title,
                'description': row.description,
                'date_finished': row.date_finished,
                'image_link': row.image_link,
                'github_link': row.github_link
            }
            projects.append(project)

    return projects

# -----------------------------------------------------------------------

# Test function to add a sample project
def _test1():
    new_project = Project(
        title="test",
        description="test",
        date_finished="test",
        image_link="test",
        github_link="test"
    )
    add_project(new_project)

# Test function to retrieve and display projects with title 'test'
def _test2():
    projects = get_projects('test')
    for project in projects:
        print(project['title'])
        print(project['description'])
        print(project['date_finished'])
        print(project['image_link'])
        print(project['github_link'])
        print()

# Test function to clear all projects from the table
def _test3():
    clear_project_table()

# Run test functions if the script is executed directly
if __name__ == '__main__':
    _test3()
    _test1()
    _test2()
