# Copyright (c) 2014, Matt Layman
"""The catalog of available templates"""

import os
import string

from handroll.exceptions import AbortError


class TemplateCatalog(object):

    DEFAULT_TEMPLATE = 'template.html'

    def __init__(self, site_path):
        self.site_path = site_path
        self._default_template_path = os.path.join(site_path,
                                                   self.DEFAULT_TEMPLATE)
        self._default = None
        self._templates = {}

    @property
    def default(self):
        """Get the default site template."""
        if self._default is None:
            self._default = StringTemplate(self._default_template_path)

        return self._default


class Template(object):

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


def has_templates(site_path):
    """Check if the site path has any templates."""
    default_template_path = os.path.join(site_path,
                                         TemplateCatalog.DEFAULT_TEMPLATE)
    if os.path.exists(default_template_path):
        return True

    # TODO: Add check for templates directory as an alternative.
    return False
