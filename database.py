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
    print("database.py: Projects table created successfully.")

# Function to add a new project to the database
def add_project(
        title, description, date_finished, image_link, github_link):
    # If the project is already in the database, do not add it
    projects = get_projects(title)
    if projects:
        print("database.py: Project already in Database")
        return
    
    new_project = Project(
        title=title,
        description=description,
        date_finished=date_finished,
        image_link=image_link,
        github_link=github_link
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
    add_project("test", "test", "test", "test", "test")

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

# Test function to remove a project from the table
def _test4():
    add_project("test2", "test", "test", "test", "test")
    remove_project("test2")

# Run test functions if the script is executed directly
if __name__ == '__main__':
    _test3()
    _test1()
    _test2()
    _test4()
