# Copyright (c) 2017, Matt Layman

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


class URLResolver(object):
    """Resolve a URL in relation to another URL."""

    def __init__(self, config, default_url):
        self._config = config
        self._default_url = default_url

    def resolve(self, base_url, path):
        """Resolve a path relative to a base URL.

        Use the default if the path is empty.
        """
        if path:
            if path.startswith('/'):
                return self._config.domain + path
            else:
                url_parts = base_url.split('/')
                url_parts[-1] = path
                return '/'.join(url_parts)
        return self._default_url
