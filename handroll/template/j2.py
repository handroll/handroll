# Copyright (c) 2016, Matt Layman

import os

import jinja2
from jinja2 import meta

from handroll.exceptions import AbortError
from handroll.i18n import _


class JinjaTemplateBuilder(object):

    def __init__(self, templates_path):
        self.templates_path = templates_path
        loader = jinja2.FileSystemLoader(templates_path)
        self._env = jinja2.Environment(
            loader=loader, trim_blocks=True, auto_reload=False)
        self._templates_modified_times = {}

    def build(self, template_path):
        """Build a Jinja template from the file path."""
        # Strip the templates path from the template path to get the relative
        # name that the ``FileSystemLoader`` wants.
        template_name = os.path.relpath(template_path, self.templates_path)
        try:
            template = self._env.get_template(template_name)
            template.last_modified = self._get_last_modified(template_name,
                                                             template_path)
            return template
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise AbortError(
                _('An error exists in the Jinja template at {template}:'
                  ' {error}').format(template=template_path, error=str(e)))

    def _get_last_modified(self, template_name, template_path=None):
        """Get the last modified time of the template.

        Use the inheritance chain to determine if anything in the chain is
        newer and should represent this template's last modified time.
        """
        if template_name in self._templates_modified_times:
            return self._templates_modified_times[template_name]

        if template_path is None:
            template_path = os.path.join(self.templates_path, template_name)

        # Assume that the current modified time of the template is best.
        last_modified = os.path.getmtime(template_path)

        # Check for any parents and then check their modified times.
        with open(template_path, 'r') as f:
            source = f.read()
        ast = self._env.parse(source, template_name, template_path)
        templates = meta.find_referenced_templates(ast)
        for parent in templates:
            if parent is None:
                # Nothing helpful can be done with None, but it may show up.
                continue

            parent_last_modified = self._get_last_modified(parent)
            if parent_last_modified > last_modified:
                # The template should look at least as recent as its parent.
                last_modified = parent_last_modified

        self._templates_modified_times[template_name] = last_modified
        return last_modified
