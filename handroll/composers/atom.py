# Copyright (c) 2016, Matt Layman

import io
import json
import os

from werkzeug.contrib.atom import AtomFeed
from werkzeug.contrib.atom import FeedEntry

from handroll import date, logger
from handroll.composers import Composer
from handroll.exceptions import AbortError
from handroll.i18n import _


class AtomComposer(Composer):
    """Compose an Atom feed from an Atom metadata file (``.atom``).

    The ``AtomComposer`` parses the metadata specified in the source file and
    produces an XML Atom feed. ``AtomComposer`` uses parameters that are needed
    by Werkzeug's ``AtomFeed`` API. Refer to the `Werkzeug documentation
    <http://werkzeug.pocoo.org/docs/contrib/atom/>`_ for all the available
    options.

    The dates in the feed should be in `RfC 3339
    <http://www.ietf.org/rfc/rfc3339.txt>`_ format (e.g.,
    ``2014-06-13T11:39:30``).

    Here is a sample feed:

    .. literalinclude:: ../sample/atom_sample.atom
    """
    output_extension = '.xml'

    def compose(self, catalog, source_file, out_dir):
        root, ext = os.path.splitext(os.path.basename(source_file))
        filename = root + self.output_extension
        output_file = os.path.join(out_dir, filename)
        if self._needs_update(source_file, output_file):
            logger.info(_('Generating Atom XML for {source_file} ...').format(
                source_file=source_file))
            feed = self._parse_feed(source_file)

            with open(output_file, 'wb') as out:
                out.write(feed.to_string().encode('utf-8'))
                out.write(b'<!-- handrolled for excellence -->\n')
        else:
            logger.debug(_('Skipping {filename} ... It is up to date.').format(
                filename=filename))

    def get_output_extension(self, filename):
        return self.output_extension

    def _needs_update(self, source_file, out_file):
        """Check if the output file needs to be updated by looking at the
        modified times of the source file and output file."""
        if self._config.force:
            return True

        if os.path.exists(out_file):
            return os.path.getmtime(source_file) > os.path.getmtime(out_file)
        else:
            # The file doesn't exist so it definitely needs to be "updated."
            return True

    def _parse_feed(self, source_file):
        try:
            with io.open(source_file, 'r', encoding='utf-8') as f:
                metadata = json.loads(f.read())

            if metadata.get('entries') is None:
                raise ValueError(_('Missing entries list.'))

            entries = metadata['entries']
            # AtomFeed expects FeedEntry objects for the entries keyword so
            # remove it from the metadata and add it after the feed is built.
            del metadata['entries']

            feed = AtomFeed(**metadata)
            [feed.add(self._make_entry(entry)) for entry in entries]
        except ValueError as error:
            raise AbortError(_('Invalid feed {source_file}: {error}').format(
                source_file=source_file, error=str(error)))

        return feed

    def _make_entry(self, data):
        # Convert dates into datetime instances.
        if 'updated' in data:
            data['updated'] = date.convert(data['updated'])

        if 'published' in data:
            data['published'] = date.convert(data['published'])

        return FeedEntry(**data)
