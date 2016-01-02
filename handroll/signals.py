# Copyright (c) 2016, Matt Layman
"""Signals fired during execution"""

from blinker import signal

frontmatter_loaded = signal('frontmatter_loaded')
pre_composition = signal('pre_composition')
post_composition = signal('post_composition')
