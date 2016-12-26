# Copyright (c) 2016, Matt Layman

import os

import jinja2

from handroll import logger
from handroll.composers import Composer
from handroll.composers.mixins import FrontmatterComposerMixin
from handroll.i18n import _


class Jinja2Composer(FrontmatterComposerMixin, Composer):
    """Compose any content from a Jinja 2 template files (``.j2``).

    The ``Jinja2Composer`` takes a template file and processes it
    through the Jinja 2 renderer. The site configuration is provided
    to the context for access to global data.

    The output file uses the same name as the source file with
    the ``.j2`` extension removed.
    """
    guess_title = False

    def compose(self, catalog, source_file, out_dir):
        filename = os.path.basename(source_file.rstrip('.j2'))
        output_file = os.path.join(out_dir, filename)
        if self._needs_update(source_file, output_file):
            logger.info(_('Generating from template {source_file} ...').format(
                source_file=source_file))
            data, source = self.get_data(source_file)
            data['config'] = self._config
            template = jinja2.Template(source)
            with open(output_file, 'wb') as out:
                out.write(template.render(data).encode('utf-8'))
                # Frontmatter loading seems to munch the final line separator.
                out.write(os.linesep.encode('utf-8'))
        else:
            logger.debug(_('Skipping {filename} ... It is up to date.').format(
                filename=filename))

    def _needs_update(self, source_file, output_file):
        """Check if the output file needs to be updated.

        Look at the modified times of the source file and output file.
        """
        if self._config.force:
            return True

        if not os.path.exists(output_file):
            return True

        return os.path.getmtime(source_file) > os.path.getmtime(output_file)

    def get_output_extension(self, filename):
        """Get the output extension.

        The composer treats the last found extension before ``.j2``
        as the file's output extension (e.g., ``source.txt.j2``
        results in ``source.txt``).
        """
        root, ext = os.path.splitext(filename.rstrip('.j2'))
        return ext
