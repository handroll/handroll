# Copyright (c) 2016, Matt Layman

from datetime import datetime
import time


def convert(date):
    """Convert a date string into a datetime instance. Assumes date string
    is RfC 3339 format."""
    time_s = time.strptime(date, '%Y-%m-%dT%H:%M:%S')
    return datetime.fromtimestamp(time.mktime(time_s))
