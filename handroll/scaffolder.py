# Copyright (c) 2015, Matt Layman

from handroll.i18n import _

BUILTIN_SCAFFOLDS = {
    'default': _('A complete site to get you going'),
}
LIST_SCAFFOLDS = 1


def get_label(scaffold):
    """Get the label for the scaffold."""
    return BUILTIN_SCAFFOLDS[scaffold]
