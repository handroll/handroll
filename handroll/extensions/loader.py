# Copyright (c) 2015, Matt Layman

from pkg_resources import iter_entry_points


class ExtensionLoader(object):
    """A loader for extensions from handroll's extension entry point."""

    def __init__(self):
        self._available_extensions = {}

    def load(self):
        """Load all available extensions from ``handroll.extensions``."""
        for entry_point in iter_entry_points('handroll.extensions'):
            cls = entry_point.load()
            self._available_extensions[entry_point.name] = cls
