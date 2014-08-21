# Copyright (c) 2014, Matt Layman
"""The catalog of available templates"""

import os
import string

from handroll.exceptions import AbortError


class Template(object):

    def __init__(self, template_path):
        """Construct a template from the given path.

        :param template_path: The path to the template source
        """

    def render(self, context):
        """Render the context as a string in whatever manner is appropriate."""
        raise NotImplementedError


class StringTemplate(Template):
    """This template class is a thin wrapper around ``string.Template`` to
    conform to the standard handroll template API."""

    def __init__(self, template_path):
        if not os.path.exists(template_path):
            raise AbortError('No template found at {0}.'.format(template_path))

        with open(template_path, 'r') as t:
            self._template = string.Template(t.read())

    def render(self, context):
        return self._template.safe_substitute(context)


class TemplateCatalog(object):

    DEFAULT_TEMPLATE = 'template.html'
    TEMPLATES_DIR = 'templates'
    TEMPLATE_TYPES = {
        '.html': StringTemplate
    }

    def __init__(self, site_path):
        self.site_path = site_path
        self._default_template_path = os.path.join(site_path,
                                                   self.DEFAULT_TEMPLATE)
        self._default = None
        self.templates_path = os.path.join(site_path, self.TEMPLATES_DIR)
        self._templates = {}

    @property
    def default(self):
        """Get the default site template."""
        if self._default is None:
            self._default = StringTemplate(self._default_template_path)

        return self._default

    def get_template(self, template_name):
        """Get the template for the given name. Abort if not found."""
        # Fetch from cache.
        if template_name in self._templates:
            return self._templates[template_name]

        template_path = os.path.join(self.templates_path, template_name)
        if not os.path.exists(template_path):
            raise AbortError('No template found at {0}.'.format(template_path))

        template = self._build_template(template_path)
        self._templates[template_name] = template
        return template

    def _build_template(self, template_path):
        """Build a template. Abort if unknown type."""
        for extension, template_type in self.TEMPLATE_TYPES.items():
            if template_path.endswith(extension):
                return template_type(template_path)

        raise AbortError('Unknown template type provided for {0}.'.format(
            template_path))


def has_templates(site_path):
    """Check if the site path has any templates."""
    default_template_path = os.path.join(site_path,
                                         TemplateCatalog.DEFAULT_TEMPLATE)
    if os.path.exists(default_template_path):
        return True

    templates_path = os.path.join(site_path, TemplateCatalog.TEMPLATES_DIR)
    if os.path.exists(templates_path):
        return True

    return False
