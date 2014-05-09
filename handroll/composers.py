# Copyright (c) 2014, Matt Layman

import os
try:
    from html import escape
except ImportError:
    from cgi import escape

import markdown

from handroll import logger


class MarkdownComposer(object):

    EXTENSIONS = [
        'codehilite',
        'fenced_code',
    ]

    def compose(self, template, source_file, out_dir):
        """Compose an HTML document by generating HTML from the Markdown source
        file, merging it with the template, and write the result to output
        directory."""
        logger.info('Generating HTML for {0} ...'.format(source_file))

        # Read the Markdown source to extract the title and content.
        data = {}
        with open(source_file, 'r') as md:
            # The title is expected to be on the first line.
            data['title'] = escape(md.readline().strip())
            source = md.read()
            data['content'] = markdown.markdown(
                source, extensions=self.EXTENSIONS, output_format='html5')

        # Merge the data with the template and write it to the out directory.
        basename = os.path.splitext(source_file.split(os.sep)[-1])[0]
        output_file = os.path.join(out_dir, basename + '.html')
        with open(output_file, 'w') as out:
            out.write(template.safe_substitute(data))
            out.write('<!-- handrolled for excellence -->\n')
