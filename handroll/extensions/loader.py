# Copyright (c) 2016, Matt Layman

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

    def get_active_extensions(self, config):
        """Get instances of active extensions."""
        extensions = []
        for extension in config.active_extensions:
            extension_cls = self._available_extensions.get(extension)
            if extension_cls is not None:
                extensions.append(extension_cls(config))
        return extensions
