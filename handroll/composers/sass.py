# Copyright (c) 2016, Matt Layman

from distutils import spawn
import os
import subprocess

from handroll import logger
from handroll.composers import Composer
from handroll.exceptions import AbortError
from handroll.i18n import _


class SassComposer(Composer):
    """Compose CSS files from Sass files (``.scss`` or ``.sass``).

    Sass is a CSS preprocessor to help manage CSS files. The Sass website has
    `great documentation <http://sass-lang.com/guide>`_ to explain how to use
    it.

    Because Sass is not written in the same language as handroll, it must be
    installed separately before it can be used. Check out the `installation
    options <http://sass-lang.com/install>`_.
    """
    output_extension = '.css'

    def __init__(self, path=None):
        self.sass = spawn.find_executable('sass', path)
        if self.sass is None:
            raise AbortError(_('Sass is not installed.'))

    def compose(self, catalog, source_file, out_dir):
        root, ext = os.path.splitext(os.path.basename(source_file))
        filename = root + self.output_extension
        output_file = os.path.join(out_dir, filename)

        logger.info(_('Generating CSS for {source_file} ...').format(
            source_file=source_file))

        command = self.build_command(source_file, output_file)
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (out, err) = process.communicate()

        if out:
            logger.debug(_('Received output from sass:\n{0}'.format(out)))

        if process.returncode != 0:
            raise AbortError(_('Sass failed to generate CSS:\n{0}').format(
                err))

    def get_output_extension(self, filename):
        return self.output_extension

    def build_command(self, source_file, output_file):
        command = [
            self.sass, '--style', 'compressed', source_file, output_file]
        return command
