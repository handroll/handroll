# Copyright (c) 2016, Matt Layman
"""The catalog of available templates"""

import os
import string

from handroll.exceptions import AbortError
from handroll.i18n import _
from handroll.template.j2 import JinjaTemplateBuilder


class Template(object):

    def render(self, context):
        """Render the context as a string in whatever manner is appropriate."""
        raise NotImplementedError

    @property
    def last_modified(self):
        """Get the the last modified time of the source of the template."""
        raise NotImplementedError


class StringTemplate(Template):
    """This template class is a thin wrapper around ``string.Template`` to
    conform to the standard handroll template API."""

    def __init__(self, template_path):
        self._last_modified = os.path.getmtime(template_path)

        with open(template_path, 'r') as t:
            self._template = string.Template(t.read())

    def render(self, context):
        return self._template.safe_substitute(context)

    @property
    def last_modified(self):
        return self._last_modified


class TemplateCatalog(object):

    DEFAULT_TEMPLATE = 'template.html'
    TEMPLATES_DIR = 'templates'

    def __init__(self, site_path, builders=None):
        self.site_path = site_path
        self._default_template_path = os.path.join(site_path,
                                                   self.DEFAULT_TEMPLATE)
        self._default = None
        self.templates_path = os.path.join(site_path, self.TEMPLATES_DIR)
        self._templates = {}
        self._builders = builders
        if builders is None:
            # Set default builders.
            self._jinja_builder = JinjaTemplateBuilder(self.templates_path)
            self._builders = {
                '.html': StringTemplate,
                '.j2': self._jinja_builder.build
            }

    @property
    def default(self):
        """Get the default site template."""
        if self._default is None:
            self._abort_if_missing(self._default_template_path)
            self._default = StringTemplate(self._default_template_path)

        return self._default

    def get_template(self, template_name):
        """Get the template for the given name. Abort if not found."""
        # Fetch from cache.
        if template_name in self._templates:
            return self._templates[template_name]

        template_path = os.path.join(self.templates_path, template_name)
        self._abort_if_missing(template_path)
        template = self._build_template(template_path)
        self._templates[template_name] = template
        return template

    def _abort_if_missing(self, template_path):
        if not os.path.exists(template_path):
            raise AbortError(_('No template found at {template_path}.').format(
                template_path=template_path))

    def _build_template(self, template_path):
        """Build a template. Abort if unknown type."""
        for extension, template_builder in self._builders.items():
            if template_path.endswith(extension):
                return template_builder(template_path)

        raise AbortError(
            _('Unknown template type provided for {template}.').format(
                template=template_path))

    def is_template(self, path):
        """Check if the path provided looks like a template."""
        if path.startswith(self.templates_path):
            return True
        if path == self._default_template_path:
            return True
        return False
