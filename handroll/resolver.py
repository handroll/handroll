# Copyright (c) 2016, Matt Layman

import os


class FileResolver(object):
    """Resolve source files to their expected output location."""

    def __init__(self, site_path, composers, config):
        self.site_path = site_path
        self.composers = composers
        self.config = config

    def as_route(self, source_path):
        """Resolve the output route of the provided source path."""
        path = os.path.relpath(source_path, self.site_path)
        return '/' + self._convert_to_url(path)

    def as_url(self, source_path):
        """Resolve the output URL of the provided source path."""
        return self.config.domain + self.as_route(source_path)

    def _convert_to_url(self, path):
        """"Convert the path to a URL path by swapping the extension."""
        composer = self.composers.select_composer_for(path)
        root, ext = os.path.splitext(path)
        return root + composer.get_output_extension(path)
