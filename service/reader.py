"""import os
import re

import dateutil.parser
import textwrap

from datetime import datetime
from flask.ext.misaka import markdown
from titlecase import titlecase
from urllib.parse import quote_plus


class Reader():

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

        metadata = self._normalize_metadata(metadata, filename)
        document = ''.join(lines[key:])
        return (metadata, document)

    def _normalize_metadata(self, metadata, file):

        def check(key):
            return key in metadata and metadata[key]

        def normalize(key, action, fallback):
            metadata[key] = action(metadata[key]) if check(key) else fallback()

        def raise_exp():
            raise KeyError

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

    def build(self, root, file):
        if file.startswith('.') or not file.endswith('.md'):
            return False

        try:
            with open(os.path.join(root, file)) as text:
                meta, content = self._parse_metadata(text.readlines(), file)
        except OSError:
            return False

        if not meta or (meta['date'] - datetime.now()).days >= 0:
            return False

        # TODO: Pass config[markdown] to the markdown parser
        html = self._embed_templating(markdown(content), meta)
        name = os.path.splitext(meta['slug'])[0] + '.jinja'

        with open(os.path.join(self.target, name), 'w') as text:
            text.write(html)

        self.meta[name] = meta
        return True

    def build_all(self):
        for root, dirs, files in os.walk(self.source):
            for file in files:
                self.build(root, file)

    def update(self, paths):
        for path in paths:
            self.build(*os.path.splitext(path))

    def clean(self):
        for name in os.listdir(self.target):
            if not name.startswith("."):
                os.remove(os.path.join(self.target, name))

        self.content = {}
"""