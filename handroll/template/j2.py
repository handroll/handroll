# Copyright (c) 2014, Matt Layman

import os

import jinja2

from handroll.exceptions import AbortError


class JinjaTemplate(jinja2.Template):
    """A wrapper around the Jinja template to access last modified dates of all
    templates in the inheritance chain.
    """
    # TODO: Extract the last modified dates via the ast and
    # ``find_referenced_templates``. Override `_parse` to do so.


class JinjaTemplateBuilder(object):

    def __init__(self, templates_path):
        self.templates_path = templates_path
        loader = jinja2.FileSystemLoader(templates_path)
        self._env = jinja2.Environment(
            loader=loader, trim_blocks=True, auto_reload=False)
        self._env.template_class = JinjaTemplate

    def build(self, template_path):
        """Build a Jinja template from the file path."""
        # Strip the templates path from the template path to get the relative
        # name that the ``FileSystemLoader`` wants.
        template_name = os.path.relpath(template_path, self.templates_path)
        try:
            return self._env.get_template(template_name)
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise AbortError(
                'An error exists in the Jinja template at {0}: {1}'.format(
                    template_path, str(e)))
