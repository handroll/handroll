# Copyright (c) 2015, Matt Layman

import markdown

from handroll.composers.generic import GenericHTMLComposer


class MarkdownComposer(GenericHTMLComposer):
    """Compose HTML from Markdown files (``.md``).

    The first line of the file will be used as the ``title`` data for the
    template. All following lines will be converted to HTML and sent to the
    template as the ``content`` data.

    The ``MarkdownComposer`` supports syntax highlighting using Pygments. Code
    can be specified using "fenced code" triple backticks.

    ::

        ```python
        class Foo(object):
            '''This sample code would be highlighted in a Python style.'''
        ```

    Use ``pygmentize`` to create your desired CSS file. Refer to the
    `Pygments documentation <http://pygments.org/docs/>`_ for more information.

    .. code-block:: bash

        $ pygmentize -S default -f html > pygments.css
    """

    EXTENSIONS = [
        'codehilite',
        'fenced_code',
    ]

    def _generate_content(self, source):
        return markdown.markdown(
            source, extensions=self.EXTENSIONS, output_format='html5')
