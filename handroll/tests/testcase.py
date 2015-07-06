# Copyright (c) 2015, Matt Layman

import unittest

from handroll.tests.factory import Factory


class TestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCase, self).__init__(methodName)
        self.factory = Factory()

    def assertIsNone(self, x):
        """Backport for Python 2.6."""
        self.assertTrue(x is None)
