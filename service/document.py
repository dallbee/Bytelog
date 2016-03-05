import os
import re

import dateutil.parser
import textwrap

from datetime import datetime
from flask.ext.misaka import markdown
from titlecase import titlecase
from urllib.parse import quote_plus
from glob2 import glob

"""
reader api:
metadata: { title*, date, keywords, description, template, path, prev, next }   (*required)
build(source, target) -> (document, metadata) parses a given item

documents api:
update(path)   creates, updates, or deletes document(s) at path appropriately
remove(path)   deletes document(s) at path
"""


class Documents():

    meta = {}
    source = ''
    target = ''

    def __init__(self, source, target):
        self.source = source
        self.target = target
        os.makedirs(self.target, exist_ok=True)

    def _parse_metadata(self, lines, filename):
        metadata = {}

        for key, line in enumerate(lines):
            result = re.match('^(\w*)[ \t]*:[ \t]*(.*)?[ \t]*$', line)

            if result is None:
                break

            metadata[result.group(1).lower()] = result.group(2)

        metadata = self._normal_metadata(metadata, filename)
        document = ''.join(lines[key:])
        return (metadata, document)

    def _normal_metadata(self, metadata, file):

        def check(key):
            return key in metadata and metadata[key]

        def normalize(key, action, fallback):
            metadata[key] = action(metadata[key]) if check(key) else fallback()

        def raise_exp():
            raise KeyError

        # TODO: Update metadata to reflect new items
        try:
            normalize('title', titlecase, raise_exp)
            normalize('date', dateutil.parser.parse, raise_exp)
            normalize('category', lambda x: x, lambda: '')
            normalize('keywords', lambda x: x.lower().split(), lambda: [])
            normalize('template', lambda x: x, lambda: 'default')
            normalize('slug', quote_plus, lambda: os.path.splitext(file)[0])
        except(KeyError, ValueError, OverflowError):
            return {}

        return metadata

    def _embed_templating(self, html, metadata):
        return textwrap.dedent('''\
            {{% extends '{template}.jinja' %}}
            {{% block content %}}
            {content}{{% endblock %}}
            ''').format(content=html, template=metadata['template'])

    def _build(self, root, file):
        # TODO: Allow other file types
        if not file.endswith('.md'):
            raise ValueError

        try:
            with open(os.path.join(root, file)) as text:
                meta, content = self._parse_metadata(text.readlines(), file)
        except OSError:
            raise ValueError

        if not meta or (meta['date'] - datetime.now()).days >= 0:
            raise ValueError

        # TODO: Pass config[markdown] to the markdown parser
        html = self._embed_templating(markdown(content), meta)
        name = os.path.splitext(meta['slug'])[0] + '.jinja'
        return (meta, html)

    def _normal_glob(self, path):
        path += '**' if path.endswith('/') else '*/**'
        return glob(path)

    def update(self, path):
        self.remove(path)
        source_path = os.path.join(self.source, path)

        for item in self._normal_glob(source_path):
            try:
                meta, html = self._build(*os.path.split(item))
                print(meta['title'])
            except ValueError:
                pass

    def remove(self, path):
        target_path = os.path.join(self.target, path)

        for item in self._normal_glob(target_path):
            os.remove(item)

        self.content = {}