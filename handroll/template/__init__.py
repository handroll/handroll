# Copyright (c) 2016, Matt Layman

import os

DEFAULT_TEMPLATE = 'template.html'
TEMPLATES_DIR = 'templates'


def has_templates(site_path):
    """Check if the site path has any templates."""
    if os.path.exists(os.path.join(site_path, DEFAULT_TEMPLATE)):
        return True

    if os.path.exists(os.path.join(site_path, TEMPLATES_DIR)):
        return True

    return False
