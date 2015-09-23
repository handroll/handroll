# Copyright (c) 2015, Matt Layman

from handroll import scaffolder
from handroll.i18n import _
from handroll.tests import TestCase


class TestScaffolder(TestCase):

    def test_default_scaffolder_label(self):
        label = scaffolder.get_label('default')
        self.assertEqual(_('A complete site to get you going'), label)
