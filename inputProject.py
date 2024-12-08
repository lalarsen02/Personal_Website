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
import datetime
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
                'imagesource_link': '',
                'imagesource_text': '',
                'youtube_link': '',
                'presentation_link': '',
                'writeup_link': '',
                'github_link': '',
                'other_links': ''
            }
            current_field = None
            description_lines = []
            other_lines = []

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
                        date_string = line[
                            len("Date Finished:"):].strip()
                        data[current_field] = datetime.datetime.strptime(
                            date_string, "%m/%d/%y")
                    elif line.startswith("Image Link:"):
                        current_field = 'image_link'
                        data[current_field] = line[
                            len("Image Link:"):].strip()
                    elif line.startswith("Image Source Link:"):
                        current_field = 'imagesource_link'
                        data[current_field] = line[
                            len("Image Source Link:"):].strip()
                    elif line.startswith("Image Source Text:"):
                        current_field = 'imagesource_text'
                        data[current_field] = line[
                            len("Image Source Text:"):].strip()
                    elif line.startswith("YouTube Link:"):
                        current_field = 'youtube_link'
                        data[current_field] = line[
                            len("YouTube Link:"):].strip()
                    elif line.startswith("Presentation Link:"):
                        current_field = 'presentation_link'
                        data[current_field] = line[
                            len("Presentation Link:"):].strip()
                    elif line.startswith("Writeup Link:"):
                        current_field = 'writeup_link'
                        data[current_field] = line[
                            len("Writeup Link:"):].strip()
                    elif line.startswith("Github Link:"):
                        current_field = 'github_link'
                        data[current_field] = line[
                            len("Github Link:"):].strip()
                    elif line.startswith("Other Links:"):
                        current_field = 'other_links'
                        other_lines = []
                    elif current_field == 'description':
                        description_lines.append(line)
                    elif current_field == 'other_links':
                        other_lines.append(line)
                
                # Join description lines into a single string
                data['description'] = "\n".join(description_lines)
                data['other_links'] = '\n'.join(other_lines)

            # project = database.get_projects(data["title"])
            # if project:
            #     print("inputProject.py: Remove and Re-add Project")
            #     database.remove_project(data['title'])
            # else:
            #     print("inputProject.py: Adding Project")

            database.add_project(
                data['title'], data['description'], data['date_finished'],
                data['image_link'], data['imagesource_text'],
                data['imagesource_link'], data['youtube_link'],
                data['presentation_link'], data['writeup_link'],
                data['github_link'], data['other_links'])

        except Exception as ex:
            print("inputProject.py: " + str(ex), file=sys.stderr)
            sys.exit(1)

    except Exception as ex:
        print("inputProject.py: " + str(ex), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
