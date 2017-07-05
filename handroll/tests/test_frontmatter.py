import inspect
import tempfile

from handroll.frontmatter import FrontmatterExtractor
from handroll.tests import TestCase


class TestFrontmatterExtractor(TestCase):

    def test_extracts(self):
        source = inspect.cleandoc("""%YAML 1.1
        ---
        title: "ØMQ: A dynamic book with surprises"
        ---
        The Content
        """)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(source.encode('utf-8'))
        extractor = FrontmatterExtractor()
        frontmatter = extractor.extract(f.name)
        self.assertEqual('ØMQ: A dynamic book with surprises', frontmatter['title'])
