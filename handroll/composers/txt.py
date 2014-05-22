# Copyright (c) 2014, Matt Layman

import io
import os
import shutil
import sys
try:
    from html import escape
except ImportError:
    from cgi import escape

try:
    import textile
except ImportError:
    pass

from handroll import logger
from handroll.composers import Composer


class TextileComposer(Composer):
    """Compose HTML from Textile files (``.textile``).

    The first line of the file will be used as the ``title`` data for the
    template. All following lines will be converted to HTML and sent to the
    template as the ``content`` data.
    """

    def compose(self, template, source_file, out_dir):
        """Compose an HTML document by generating HTML from the Textile source
        file, merging it with the template, and write the result to output
        directory."""
        if sys.version_info.major == 3:
            logger.error('Sorry. Textile does not yet support Python 3.')
            return

        logger.info('Generating HTML for {0} ...'.format(source_file))

        # Read the Textile source to extract the title and content.
        data = {}
        with io.open(source_file, 'r', encoding='utf-8') as f:
            # The title is expected to be on the first line.
            data['title'] = escape(f.readline().strip())
            source = f.read()
            data['content'] = textile.textile(source)

        # Merge the data with the template and write it to the out directory.
        root, _ = os.path.splitext(os.path.basename(source_file))
        output_file = os.path.join(out_dir, root + '.html')
        with open(output_file, 'wb') as out:
            out.write(template.safe_substitute(data).encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')
