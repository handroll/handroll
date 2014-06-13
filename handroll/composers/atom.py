# Copyright (c) 2014, Matt Layman

import os
import sys

from werkzeug.contrib.atom import AtomFeed

from handroll import logger
from handroll.composers import Composer


class AtomComposer(Composer):
    """Compose an Atom feed from an Atom metadata file (``.atom``).

    The ``AtomComposer`` parses the metadata specified in the source file and
    produces an XML Atom feed. ``AtomComposer`` uses parameters that are needed
    by Werkzeug's ``AtomFeed`` API. Refer to the `Werkzeug documentation
    <http://werkzeug.pocoo.org/docs/contrib/atom/>`_ for all the available
    options.
    """

    def compose(self, template, source_file, out_dir):
        logger.info('Generating Atom XML for {0} ...'.format(source_file))
        # TODO: Determine what the input file will look like (YAML? JSON?).
        try:
            feed = AtomFeed('Dummy Title', id='temporary')
        except ValueError as error:
            logger.error('Invalid feed {0}: {1}'.format(
                source_file, error.message))
            sys.exit('Incomplete.')

        root, _ = os.path.splitext(os.path.basename(source_file))
        output_file = os.path.join(out_dir, root + '.xml')
        with open(output_file, 'wb') as out:
            out.write(feed.to_string().encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')
