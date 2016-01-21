from flask.ext.misaka import Misaka, markdown
import os

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

"""


class Reader():

    content = {}
    source = ''
    target = ''

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def _parse_metadata(self, document):
        metadata = {}


    def build(self):
        # make a directory for each category
        # prepend the correct template text

        for root, dirs, files in os.walk(self.source):
            for filename in files:
                if filename.startswith("."):
                    continue
                with open(os.path.join(root, filename)) as text:
                    content = markdown(text.read())
                    filename = os.path.splitext(filename)[0] + '.jinja'
                with open(os.path.join(self.target, filename), 'w') as text:
                    text.write(content)


    def clean(self):
        self.content = {}

        for root, dirs, files in os.walk(self.target, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
