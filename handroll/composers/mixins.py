# Copyright (c) 2016, Matt Layman

import io
try:
    from html import escape
except ImportError:
    from cgi import escape
import os

import yaml
from yaml.scanner import ScannerError

from handroll import signals
from handroll.exceptions import AbortError
from handroll.i18n import _


class FrontmatterComposerMixin(object):
    """Mixin the ability to extract frontmatter from a source file."""
    document_marker = '---' + os.linesep
    guess_title = True

    def get_data(self, source_file):
        """Get data and source from the source file."""
        data = {}
        with io.open(source_file, 'r', encoding='utf-8') as f:
            # The first line determines whether to look for front matter.
            first = f.readline().strip()
            source = f.read()

            if self._has_frontmatter(first):
                data, source = self._split_content_with_frontmatter(
                    first, source, source_file)
                signals.frontmatter_loaded.send(source_file, frontmatter=data)
            elif self.guess_title:
                # This is a plain file so pull title from the first line.
                data['title'] = escape(first)
            else:
                f.seek(0)
                source = f.read()

        return data, source

    def _has_frontmatter(self, first_line):
        """Check if the document has any front matter. handroll only supports
        front matter from YAML documents."""
        return first_line.startswith(('%YAML', '---'))

    def _split_content_with_frontmatter(self, first, source, source_file):
        """Separate frontmatter from source material."""
        max_splits = 1
        # With a directive present, there must be two document markers.
        if first.startswith('%YAML'):
            max_splits = 2
        content = source.split(self.document_marker, max_splits)

        try:
            data = yaml.load(content[max_splits - 1])
        except ScannerError as ex:
            raise AbortError(_(
                'There is invalid YAML in the frontmatter: {details}').format(
                    details=str(ex)))
        try:
            source = content[max_splits]
        except IndexError:
            raise AbortError(_('A YAML marker was missing in {source}').format(
                source=source_file))

        if 'title' in data:
            data['title'] = escape(data['title'])

        return data, source
