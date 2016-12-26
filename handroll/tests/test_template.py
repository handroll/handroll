# Copyright (c) 2016, Matt Layman

import os
import tempfile
import unittest

import jinja2

from handroll.exceptions import AbortError
from handroll import template
from handroll.template.catalog import StringTemplate
from handroll.template.catalog import TemplateCatalog
from handroll.template.j2 import JinjaTemplateBuilder


class TestJinjaTemplateBuilder(unittest.TestCase):

    def setUp(self):
        self.templates = tempfile.mkdtemp()
        self.builder = JinjaTemplateBuilder(self.templates)
        self.base_file = os.path.join(self.templates, 'base.j2')
        open(self.base_file, 'w').close()

    def test_builds_template(self):
        template = self.builder.build(self.base_file)
        self.assertTrue(isinstance(template, jinja2.Template))

    def test_aborts_with_bad_template(self):
        with open(self.base_file, 'w') as f:
            f.write('{%')  # No closing template marker
        with self.assertRaises(AbortError):
            self.builder.build(self.base_file)

    def test_last_modified_with_newer_parent(self):
        template_file = os.path.join(self.templates, 'derived.j2')
        with open(template_file, 'w') as f:
            f.write('{% extends "base.j2" %}')
        # Fast file systems make mtime equal for both files. Set to the future.
        template_mtime = os.path.getmtime(template_file)
        future = template_mtime + 1
        os.utime(self.base_file, (future, future))

        template = self.builder.build(template_file)
        self.assertEqual(
            os.path.getmtime(self.base_file), template.last_modified)

    def test_skips_nonetype_parent(self):
        with open(self.base_file, 'w') as f:
            f.write('{% include helper %}')  # Non-existent "parent"
        template = self.builder.build(self.base_file)
        self.assertTrue(isinstance(template, jinja2.Template))

    def test_gets_cached_modified_time(self):
        template = self.builder.build(self.base_file)
        template = self.builder.build(self.base_file)
        self.assertTrue(isinstance(template, jinja2.Template))


class TestStringTemplate(unittest.TestCase):

    def test_template_last_modified(self):
        fh, path = tempfile.mkstemp()
        expected = os.path.getmtime(path)
        template = StringTemplate(path)
        self.assertEqual(expected, template.last_modified)


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
        from handroll.template.catalog import Template
        template = Template()
        with self.assertRaises(NotImplementedError):
            template.render({})

    def test_last_modified_not_implemented(self):
        from handroll.template.catalog import Template
        template = Template()
        with self.assertRaises(NotImplementedError):
            template.last_modified

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
        with self.assertRaises(AbortError):
            catalog.default

    def test_fails_to_get_template(self):
        catalog = self._make_one()
        with self.assertRaises(AbortError):
            catalog.get_template('sad.html')

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
        with self.assertRaises(AbortError):
            catalog.get_template('confused.bogus')

    def test_is_default_template(self):
        catalog = self._make_one()
        default = os.path.join(self.site_path, 'template.html')
        self.assertTrue(catalog.is_template(default))

    def test_is_template_in_templates_directory(self):
        catalog = self._make_one()
        path = os.path.join(catalog.templates_path, 'foundme.html')
        self.assertTrue(catalog.is_template(path))

    def test_is_not_a_template(self):
        catalog = self._make_one()
        self.assertFalse(catalog.is_template('nope'))


class TestTemplateFunctions(unittest.TestCase):

    def test_has_default_template(self):
        site = tempfile.mkdtemp()
        open(os.path.join(site, 'template.html'), 'w').close()

        self.assertTrue(template.has_templates(site))

    def test_has_templates_directory(self):
        site = tempfile.mkdtemp()
        os.mkdir(os.path.join(site, 'templates'))

        self.assertTrue(template.has_templates(site))
