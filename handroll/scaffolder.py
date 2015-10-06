# Copyright (c) 2015, Matt Layman

import os

from handroll.exceptions import AbortError
from handroll.i18n import _

BUILTIN_SCAFFOLDS = {
    'default': _('A complete site to get you going'),
}
LIST_SCAFFOLDS = 1


def make(scaffold, site):
    """Use the given scaffold to make a site or list what is available."""
    if scaffold == LIST_SCAFFOLDS:
        list_scaffolds()
    else:
        make_scaffold(scaffold, site)


def list_scaffolds():
    """List out all available scaffolds."""
    print(_('Available scaffolds:\n'))
    for scaffold in sorted(BUILTIN_SCAFFOLDS.keys()):
        print(display_scaffold(scaffold, get_label(scaffold)))
    print('')


def display_scaffold(scaffold, label):
    """Display a scaffold in a consistent way for listing."""
    return '  {0: <12}| {1}'.format(scaffold, label)


def get_label(scaffold):
    """Get the label for the scaffold."""
    return BUILTIN_SCAFFOLDS[scaffold]


def make_scaffold(scaffold, site):
    """Make a site from the scaffold."""
    if scaffold not in BUILTIN_SCAFFOLDS:
        raise AbortError(_('There is no {scaffold} scaffold.'.format(
            scaffold=scaffold)))
    if os.path.exists(site):
        raise AbortError(_('{site} already exists.'.format(site=site)))
    os.makedirs(site)
    # TODO: populate the site with content from the scaffold.
