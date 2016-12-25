# Copyright (c) 2016, Matt Layman

import os

from handroll import logger
from handroll.composers import Composer
from handroll.composers.mixins import FrontmatterComposerMixin
from handroll.i18n import _


class GenericHTMLComposer(FrontmatterComposerMixin, Composer):
    """A template class that performs basic handling on a source file

    The title will be extracted from the first line and the remaining source
    lines will be passed to a template method for further processing.
    """
    output_extension = '.html'

    def compose(self, catalog, source_file, out_dir):
        """Compose an HTML document by generating HTML from the source
        file, merging it with a template, and write the result to output
        directory."""
        data, source = self.get_data(source_file)

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

    def get_output_extension(self, filename):
        return self.output_extension

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

    def _needs_update(self, template, source_file, output_file):
        """Check if the output file needs to be updated by looking at the
        modified times of the template, source file, and output file."""
        if self._config.force:
            return True

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
