# Copyright (c) 2016, Matt Layman


class AbortError(Exception):
    """Any fatal errors that would prevent handroll from proceeding should
    signal with the ``AbortError`` exception."""
