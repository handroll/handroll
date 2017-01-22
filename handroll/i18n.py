# Copyright (c) 2017, Matt Layman

import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('handroll', localedir, fallback=True)
_ = translate.gettext
