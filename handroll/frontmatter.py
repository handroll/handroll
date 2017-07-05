from handroll.composers.mixins import FrontmatterComposerMixin


class FrontmatterExtractor(FrontmatterComposerMixin):
    """Extract frontmatter from a source file."""

    def extract(self, source_file):
        data, source = self.get_data(source_file)
        return data
