# Copyright (c) 2015, Matt Layman

import io
import os
import re
try:
    from html import escape
except ImportError:
    from cgi import escape

import yaml

from handroll import logger, signals
from handroll.composers import Composer
from handroll.i18n import _


class GenericHTMLComposer(Composer):
    """A template class that performs basic handling on a source file

    The title will be extracted from the first line and the remaining source
    lines will be passed to a template method for further processing.
    """
    output_extension = '.html'

    # A pattern to get source content from a file with YAML front matter.
    yaml_scanner = re.compile(r""".*?    # YAML header
                                  ---
                                  .*?    # front matter
                                  ---\n
                                  (?P<markup>.*)""",
                              re.DOTALL | re.VERBOSE)

    def compose(self, catalog, source_file, out_dir):
        """Compose an HTML document by generating HTML from the source
        file, merging it with a template, and write the result to output
        directory."""
        data, source = self._get_data(source_file)

        template = self.select_template(catalog, data)

        # Determine the output filename.
        root, ext = os.path.splitext(os.path.basename(source_file))
        filename = root + self.output_extension
        output_file = os.path.join(out_dir, filename)

        if self._needs_update(template, source_file, output_file):
            logger.info(_('Generating HTML for {source_file} ...').format(
                source_file=source_file))
            data['content'] = self._generate_content(source)
            self._render_to_output(template, data, output_file)
        else:
            logger.debug(_('Skipping {filename} ... It is up to date.').format(
                filename=filename))

    def select_template(self, catalog, data):
        """Select a template from the catalog based on the source file's data.
        """
        if 'template' in data:
            return catalog.get_template(data['template'])
        else:
            return catalog.default

    def _generate_content(self, source):
        """Generate the content from the provided source data."""
        raise NotImplementedError

    def _get_data(self, source_file):
        """Get data and source from the source file to pass to the template."""
        data = {}
        with io.open(source_file, 'r', encoding='utf-8') as f:
            # The first line determines whether to look for front matter.
            first = f.readline().strip()
            source = f.read()

            if self._has_frontmatter(first):
                documents = yaml.load_all(source)
                data = next(documents)
                if 'title' in data:
                    data['title'] = escape(data['title'])
                signals.frontmatter_loaded.send(source_file, frontmatter=data)

                # Don't pass all file content to the composer. Find the markup.
                match = re.search(self.yaml_scanner, source)
                if match:
                    source = match.group('markup')
            else:
                # This is a plain file so pull title from the first line.
                data['title'] = escape(first)

        return data, source

    def _has_frontmatter(self, first_line):
        """Check if the document has any front matter. handroll only supports
        front matter from YAML documents."""
        return first_line.startswith('%YAML')

    def _needs_update(self, template, source_file, output_file):
        """Check if the output file needs to be updated by looking at the
        modified times of the template, source file, and output file."""
        out_modified_time = None
        if os.path.exists(output_file):
            out_modified_time = os.path.getmtime(output_file)
        else:
            # The file doesn't exist so it definitely needs to be "updated."
            return True

        if os.path.getmtime(source_file) > out_modified_time:
            return True

        if template.last_modified > out_modified_time:
            return True

        return False

    def _render_to_output(self, template, data, output_file):
        """Render the template and data to the output file."""
        with open(output_file, 'wb') as out:
            out.write(template.render(data).encode('utf-8'))
            out.write(b'<!-- handrolled for excellence -->\n')
