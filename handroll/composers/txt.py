# Copyright (c) 2014, Matt Layman

import sys

try:
    import textile
except ImportError:
    # FIXME: textile not supported on Python 3.
    pass

from handroll import logger
from handroll.composers import GenericHTMLComposer


class TextileComposer(GenericHTMLComposer):
    """Compose HTML from Textile files (``.textile``).

    The first line of the file will be used as the ``title`` data for the
    template. All following lines will be converted to HTML and sent to the
    template as the ``content`` data.
    """

    def compose(self, template, source_file, out_dir):
        # Python 2.6 does not recognize the `major` attribute of version info.
        if sys.version_info[0] == 3:
            logger.error('Sorry. Textile does not yet support Python 3.')
            return

        super(TextileComposer, self).compose(template, source_file, out_dir)

    def _generate_content(self, source):
        return textile.textile(source)
