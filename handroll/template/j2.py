# Copyright (c) 2014, Matt Layman

import os

import jinja2

from handroll.exceptions import AbortError


class JinjaTemplateBuilder(object):

    def __init__(self, templates_path):
        self.templates_path = templates_path
        loader = jinja2.FileSystemLoader(templates_path)
        self._env = jinja2.Environment(
            loader=loader, trim_blocks=True, auto_reload=False)

    def build(self, template_path):
        """Build a Jinja template from the file path."""
        # Strip the templates path from the template path to get the relative
        # name that the ``FileSystemLoader`` wants.
        template_name = os.path.relpath(template_path, self.templates_path)
        try:
            template = self._env.get_template(template_name)
            # FIXME: This is the naive implementation because it does not
            # factor in the inheritence that is part of Jinja templates (e.g.,
            # if a base template was modified, this template would not notice).
            template.last_modified = os.path.getmtime(template_path)
            return template
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise AbortError(
                'An error exists in the Jinja template at {0}: {1}'.format(
                    template_path, str(e)))
