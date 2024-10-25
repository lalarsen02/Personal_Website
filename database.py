# !/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Louis Larsen
#-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
import dotenv

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ.get('DATABASE_URL')
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

Base = sqlalchemy.orm.declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    date_finished = sqlalchemy.Column(sqlalchemy.String)
    image_link = sqlalchemy.Column(sqlalchemy.String)
    github_link = sqlalchemy.Column(sqlalchemy.String)

_engine = sqlalchemy.create_engine(_DATABASE_URL)

#-----------------------------------------------------------------------

def create_project_table():
    Base.metadata.create_all(_engine)
    print("Projects table created successfully.")

def add_project(new_project):

    with sqlalchemy.orm.Session(_engine) as session:
        session.add(new_project)
        session.commit()

    print("Project added successfully.")

def clear_project_table():

    with sqlalchemy.orm.Session(_engine) as session:
        session.query(Project).delete()
        session.commit()
    
    print("All projects cleared from the table")

def get_projects(title):

    projects = []

    with sqlalchemy.orm.Session(_engine) as session:

        query = session.query(Project).filter(
            Project.title.ilike(title+'%')
        )

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

#-----------------------------------------------------------------------

def _test1():
    new_project = Project(
        title="test",
        description="test",
        date_finished="test",
        image_link="test",
        github_link="test"
    )

    add_project(new_project)

def _test2():
    projects = get_projects('test')
    for project in projects:
        print(project['title'])
        print(project['description'])
        print(project['date_finished'])
        print(project['image_link'])
        print(project['github_link'])
        print()

def _test3():
    clear_project_table()

if __name__ == '__main__':
    _test3()
    _test1()
    _test2()
