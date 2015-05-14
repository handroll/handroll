# Copyright (c) 2015, Matt Layman

from handroll import signals


class Extension(object):
    """A base extension which hooks handler methods to handroll's signals."""

    handle_frontmatter_loaded = False

    def __init__(self, config):
        self._config = config
        # Handler functions are put in a dictionary to keep references to them.
        # Blinker behaves in strange ways without the references.
        self._handlers = {}

        if self.handle_frontmatter_loaded:
            def _handle_frontmatter_loaded(source_file, **kwargs):
                self.on_frontmatter_loaded(source_file, kwargs['frontmatter'])
            self._handlers['frontmatter_loaded'] = _handle_frontmatter_loaded
            signals.frontmatter_loaded.connect(_handle_frontmatter_loaded)

    def on_frontmatter_loaded(self, source_file, frontmatter):
        """Handle the ``frontmatter_loaded`` signal.

        Activate this handler by setting ``handle_frontmatter_loaded``
        to ``True`` in the extension subclass.

        :param source_file: Absolute path of the source file
        :param frontmatter: Dictionary of parsed frontmatter
        """
        raise NotImplementedError
