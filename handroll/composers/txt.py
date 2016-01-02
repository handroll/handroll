# Copyright (c) 2016, Matt Layman

import textile

from handroll.composers.generic import GenericHTMLComposer


class TextileComposer(GenericHTMLComposer):
    """Compose HTML from Textile files (``.textile``).

    The first line of the file will be used as the ``title`` data for the
    template. All following lines will be converted to HTML and sent to the
    template as the ``content`` data.
    """

    def _generate_content(self, source):
        return textile.textile(source)
