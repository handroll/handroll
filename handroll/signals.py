# Copyright (c) 2015, Matt Layman
"""Signals fired during execution"""

from blinker import signal

frontmatter_loaded = signal('frontmatter_loaded')
