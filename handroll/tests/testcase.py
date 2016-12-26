# Copyright (c) 2016, Matt Layman

import unittest

from handroll.tests.factory import Factory


class TestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCase, self).__init__(methodName)
        self.factory = Factory()
