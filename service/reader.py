from flask.ext.misaka import Misaka, markdown
from flask import current_app
import os
from dateutil import parser
from datetime import datetime
import urllib
import re

"""
Functions:

parse_metadata

"""



""" Metadata

Title:
Date:
Category: 
Tags:
Slug: 
Description:
Template: 


PRIVATE Metadata:
metadata['folder']
"""


class Reader():

    content = {}
    source = ''
    target = ''


    def __init__(self, source, target):
        self.source = source
        self.target = target


    def _parse_metadata(self, lines, filename):
        metadata = {
            filename: filename
        }

        for key, line in enumerate(lines):
            result = re.fullmatch('(\w*)[ \t]*:[ \t]*(.*)?[ \t]*', line)

            if result is None:
                break

            metadata[result.group(1).lower()] = result.group(2)
            metadata = self._normalize_metadata(metadata)

        document = ''.join(lines[key:])
        print(metadata)
        return (metadata, document)


    def _normalize_metadata(self, metadata):
        # Fill with default metadata: slug->filename, category->'', template->default
        if slug in metadata and metadata['slug']:
            metadata['slug'] = urllib.parse.quote_plus(metadata['slug']).lower()
        else:
            metadata['slug'] = urllib.parse.quote_plus(metadata['filename'])

        if category in metadata:
            metadata['category'] =  

        return metadata


    def build(self):
        # make a directory for each category
        # prepend the correct template text

        for root, dirs, files in os.walk(self.source):
            for filename in files:
                
                # Save on parsing time by skipping hidden & non-markdown files
                if filename.startswith('.') and filename.endswith('.md'):
                    continue

                with open(os.path.join(root, filename)) as text:
                    metadata, content = self._parse_metadata(text.readlines(), filename)

                # Verify that the article should be published
                if not metadata or (metadata['date'] - datetime.now())[0] >= 0:
                    continue

                # TODO: Pass config[markdown] to the markdown parser
                html = markdown(content)

                # Create the file at its correct location
                filename = os.path.splitext(filename)[0] + '.jinja'
                os.makedirs(os.path.join(self.target, metadata['folder']))
                with open(os.path.join(self.target, metadata['folder'], filename), 'w') as text:
                    text.write(content)


    def clean(self):
        self.content = {}

        for root, dirs, files in os.walk(self.target, topdown=False):
            for name in files:
                if not name.startswith('.')
                    os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
