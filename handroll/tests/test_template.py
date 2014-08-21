# Copyright (c) 2014, Matt Layman

import os
import tempfile
import unittest

from handroll.exceptions import AbortError
from handroll.template import StringTemplate
from handroll.template import TemplateCatalog


class TestTemplateCatalog(unittest.TestCase):

    def setUp(self):
        self.site_path = tempfile.mkdtemp()

    def _make_one(self):
        return TemplateCatalog(self.site_path)

    def _make_one_with_template(self, template_name):
        catalog = self._make_one()
        os.mkdir(catalog.templates_path)
        template = os.path.join(catalog.templates_path, template_name)
        with open(template, 'w') as f:
            f.write('Does not matter.')
        return catalog

    def test_render_not_implemented(self):
        from handroll.template import Template
        template = Template('foobar')
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

    def test_fails_to_get_template(self):
        catalog = self._make_one()
        self.assertRaises(AbortError, catalog.get_template, 'sad.html')

    def test_gets_template(self):
        catalog = self._make_one_with_template('happy.html')
        template = catalog.get_template('happy.html')
        self.assertTrue(isinstance(template, StringTemplate))

    def test_caches_template(self):
        catalog = self._make_one_with_template('happy.html')
        first = catalog.get_template('happy.html')
        second = catalog.get_template('happy.html')
        self.assertEqual(first, second)

    def test_fails_on_bad_template_type(self):
        catalog = self._make_one_with_template('confused.bogus')
        self.assertRaises(AbortError, catalog.get_template, 'confused.bogus')
