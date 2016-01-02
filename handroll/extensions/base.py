# Copyright (c) 2016, Matt Layman

from handroll import signals


class Extension(object):
    """A base extension which hooks handler methods to handroll's signals."""

    handle_frontmatter_loaded = False
    handle_pre_composition = False
    handle_post_composition = False

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

        if self.handle_post_composition:
            def _handle_post_composition(director, **kwargs):
                self.on_post_composition(director)
            self._handlers['post_composition'] = _handle_post_composition
            signals.post_composition.connect(_handle_post_composition)

        if self.handle_pre_composition:
            def _handle_pre_composition(director, **kwargs):
                self.on_pre_composition(director)
            self._handlers['pre_composition'] = _handle_pre_composition
            signals.pre_composition.connect(_handle_pre_composition)

    def on_frontmatter_loaded(self, source_file, frontmatter):
        """Handle the ``frontmatter_loaded`` signal.

        Activate this handler by setting ``handle_frontmatter_loaded``
        to ``True`` in the extension subclass.

        :param source_file: Absolute path of the source file
        :param frontmatter: Dictionary of parsed frontmatter
        """
        raise NotImplementedError()

    def on_pre_composition(self, director):
        """Handle the ``pre_composition`` signal.

        Activate this handler by setting ``handle_pre_composition``
        to ``True`` in the extension subclass.

        :param director: The director instance
        """
        raise NotImplementedError()

    def on_post_composition(self, director):
        """Handle the ``post_composition`` signal.

        Activate this handler by setting ``handle_post_composition``
        to ``True`` in the extension subclass.

        :param director: The director instance
        """
        raise NotImplementedError()
