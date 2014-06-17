# Copyright (c) 2014, Matt Layman

from datetime import datetime
import io
import json
import os
import sys
import time

from werkzeug.contrib.atom import AtomFeed
from werkzeug.contrib.atom import FeedEntry

from handroll import logger
from handroll.composers import Composer


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

    def compose(self, template, source_file, out_dir):
        logger.info('Generating Atom XML for {0} ...'.format(source_file))
        feed = self._parse_feed(source_file)

        root, _ = os.path.splitext(os.path.basename(source_file))
        output_file = os.path.join(out_dir, root + '.xml')
        with open(output_file, 'wb') as out:
            out.write(feed.to_string().encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')

    def _parse_feed(self, source_file):
        try:
            with io.open(source_file, 'r', encoding='utf-8') as f:
                metadata = json.loads(f.read())

            if metadata.get('entries') is None:
                raise ValueError('Missing entries list.')

            entries = metadata['entries']
            # AtomFeed expects FeedEntry objects for the entries keyword so
            # remove it from the metadata and add it after the feed is built.
            del metadata['entries']

            feed = AtomFeed(**metadata)
            [feed.add(self._make_entry(entry)) for entry in entries]
        except ValueError as error:
            logger.error('Invalid feed {0}: {1}'.format(
                source_file, error.message))
            sys.exit('Incomplete.')

        return feed

    def _make_entry(self, data):
        # Convert dates into datetime instances.
        if 'updated' in data:
            data['updated'] = self._convert_date(data['updated'])

        if 'published' in data:
            data['published'] = self._convert_date(data['published'])

        return FeedEntry(**data)

    def _convert_date(self, date):
        """Convert a date string into a datetime instance. Assumes date string
        is RfC 3389 format."""
        time_s = time.strptime(date, '%Y-%m-%dT%H:%M:%S')
        return datetime.fromtimestamp(time.mktime(time_s))
