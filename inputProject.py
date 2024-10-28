# !/usr/bin/env python

# -----------------------------------------------------------------------
# inputProject.py
# Author: Louis Larsen
# -----------------------------------------------------------------------

# Takes in a txt file, turns it into a Project Object, and adds it to the
# database

# -----------------------------------------------------------------------

import sys
import argparse
import database

# -----------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog='inputProject.py',
        description=(
            "Takes in a txt file, turns it into a Project Object, and "
            + "adds it to the database"
        ),
        allow_abbrev=False
    )

    parser.add_argument(
        'filePath',
        help="The path to the txt file that you would like to insert")
    return parser

def main():
    try: 
        parser = parse_args()
        args = parser.parse_args()
        filepath = args.filePath

        try:
            data = {
                'title': '',
                'description': '',
                'date_finished': '',
                'image_link': '',
                'github_link': ''
            }
            current_field = None
            description_lines = []

            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("Title:"):
                        current_field = 'title'
                        data[current_field] = line[
                            len("Title:"):].strip()
                    elif line.startswith("Description:"):
                        current_field = 'description'
                        description_lines = []
                    elif line.startswith("Date Finished:"):
                        current_field = 'date_finished'
                        data[current_field] = line[
                            len("Date Finished:"):].strip()
                    elif line.startswith("Image Link:"):
                        current_field = 'image_link'
                        data[current_field] = line[
                            len("Image Link:"):].strip()
                    elif line.startswith("Github Link:"):
                        current_field = 'github_link'
                        data[current_field] = line[
                            len("Github Link:"):].strip()
                    elif current_field == 'description':
                        description_lines.append(line)
                
                # Join description lines into a single string
                data['description'] = "\n".join(description_lines)

            project = database.get_projects(data["title"])
            if project:
                print("inputProject.py: Remove and Re-add Project")
                database.remove_project(data['title'])
                database.add_project(data['title'],
                                    data['description'],
                                    data['date_finished'],
                                    data['image_link'],
                                    data['github_link'])
            else:
                print("inputProject.py: Adding Project")
                database.add_project(data['title'],
                                    data['description'],
                                    data['date_finished'],
                                    data['image_link'],
                                    data['github_link'])

        except Exception as ex:
            print("inputProject.py: " + str(ex), file=sys.stderr)
            sys.exit(1)

    except Exception as ex:
        print("inputProject.py: " + str(ex), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
