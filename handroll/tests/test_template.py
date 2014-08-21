# Copyright (c) 2014, Matt Layman

import os
import tempfile
import unittest

from handroll.exceptions import AbortError
from handroll.template import TemplateCatalog


class TestTemplateCatalog(unittest.TestCase):

    def setUp(self):
        self.site_path = tempfile.mkdtemp()

    def _make_one(self):
        return TemplateCatalog(self.site_path)

    def test_render_not_implemented(self):
        from handroll.template import Template
        template = Template()
        self.assertRaises(NotImplementedError, template.render, {})

    def test_renders_default(self):
        """Test rendering a default template."""
        content = '<html>${title}${content}</html>\n'
        with open(os.path.join(self.site_path, 'template.html'), 'w') as f:
            f.write(content)

        catalog = self._make_one()
        template = catalog.default
        self.assertEqual(template.render({'title': 'foo', 'content': 'bar'}),
                         '<html>foobar</html>\n')

    def test_aborts_missing_default(self):
        catalog = self._make_one()

        def get_default():  # Function hack to test property exception
            catalog.default
        self.assertRaises(AbortError, get_default)
