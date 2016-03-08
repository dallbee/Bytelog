import hashlib
import os
import re

import dateutil.parser
import textwrap

from datetime import datetime
from flask.ext.misaka import markdown
from glob2 import glob
from logging import error
from logging import info
from logging import warning
from titlecase import titlecase
from urllib.parse import quote_plus

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

    def _parse_metadata(self, lines):
        meta = {}

        for key, line in enumerate(lines):
            result = re.match('^(\w*)[ \t]*:[ \t]*(.*)?[ \t]*$', line)

            if not result:
                break

            meta[result.group(1).lower()] = result.group(2)

        return (self._normal_metadata(meta), ''.join(lines[key:]))

    def _normal_metadata(self, meta):

        def check(key):
            return key in meta and meta[key]

        def clean(key, action, default):
            meta[key] = action(meta[key]) if check(key) else default()

        def raise_exp():
            raise KeyError

        try:
            clean('title', titlecase, raise_exp)
            clean('author', titlecase, lambda: None)
            clean('date', dateutil.parser.parse, raise_exp)
            clean('keywords', lambda x: x.lower().split(), lambda: [])
            clean('template', lambda x: x, lambda: 'default')
            clean('prev', quote_plus, lambda: None)
            clean('next', quote_plus, lambda: None)
        except(KeyError, ValueError, OverflowError) as e:
            warning("Unable to parse metadata: {}".format(e))
            return {}

        return meta

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
            with open(os.path.join(root, file)) as f:
                meta, content = self._parse_metadata(f.readlines())
        except OSError as e:
            error(e)
            raise ValueError

        if not meta:
            raise ValueError

        if (meta['date'] - datetime.now()).days >= 0:
            info("Skipping {} until {}".format(file, meta['date']))
            raise ValueError

        # TODO: Pass config[markdown] to the markdown parser
        return (meta, self._embed_templating(markdown(content), meta))

    def _normal_glob(self, path):
        path += '*/**' if os.path.isdir(path) else '**'
        return glob(path)

    # TODO: Remove content/ prefix from names
    def update(self, path=''):
        self.remove(path)
        source_path = os.path.join(self.source, path)

        for file in self._normal_glob(source_path):
            print(file)
            try:
                meta, html = self._build(*os.path.split(file))
            except ValueError:
                continue

            target_path = os.path.join(self.target, os.path.splitext(file)[0])
            os.makedirs(os.path.split(target_path)[0], exist_ok=True)

            try:
                print(target_path)
                with open(target_path + '.jinja', 'w') as f:
                    f.write(html)
                    self.meta[file] = meta
                    info("Written {} to cache".format(target_path))
            except OSError as e:
                error(e)

    def remove(self, path=''):
        target_path = os.path.join(self.target, path)
        glob_paths = self._normal_glob(target_path)

        for item in glob_paths:
            if os.path.isfile(item):
                try:
                    os.remove(item)
                except OSError as e:
                    error(e)

        for item in glob_paths:
            if os.path.isdir(item):
                try:
                    os.rmdir(item)
                except OSError as e:
                    error(e)

        self.meta = {}
