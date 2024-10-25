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

class Description(Base):
    __tablename__ = 'descriptions'
    title = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String)

_engine = sqlalchemy.create_engine(_DATABASE_URL)

#-----------------------------------------------------------------------

def get_descriptions(title):

    descriptions = []

    with sqlalchemy.orm.Session(_engine) as session:

        query = session.query(Description).filter(
            Description.description.ilike(title+'%')
        )

        table = query.all()
        for row in table:
            description = {
                'title': row.title,
                'description': row.description
                }
            descriptions.append(description)

    return descriptions

#-----------------------------------------------------------------------

def _test():
    descriptions = get_descriptions('test')
    for description in descriptions:
        print(description['title'])
        print(description['description'])
        print()

if __name__ == '__main__':
    _test()
