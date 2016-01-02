# Copyright (c) 2016, Matt Layman

from docutils.core import publish_parts

from handroll.composers.generic import GenericHTMLComposer


class ReStructuredTextComposer(GenericHTMLComposer):
    """Compose HTML from reStructuredText files (``.rst``).

    The first line of the file will be used as the ``title`` data for the
    template. All following lines will be converted to HTML and sent to the
    template as the ``content`` data.
    """

    def _generate_content(self, source):
        return publish_parts(source, writer_name='html')['html_body']
