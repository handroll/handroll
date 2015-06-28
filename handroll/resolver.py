# Copyright (c) 2015, Matt Layman

import os


class FileResolver(object):
    """Resolve source files to their expected output location."""

    def __init__(self, site_path, composers, config):
        self.site_path = site_path
        self.composers = composers
        self.config = config

    def as_url(self, source_path):
        """Resolve the output URL of the provided source path."""
        path = os.path.relpath(source_path, self.site_path)
        url_path = self._convert_to_url(path)
        return "/".join([self.config.domain, url_path])

    def _convert_to_url(self, path):
        """"Convert the path to a URL path by swapping the extension."""
        composer = self.composers.select_composer_for(path)
        root, ext = os.path.splitext(path)
        return root + composer.output_extension
