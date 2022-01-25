# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from io import StringIO
import mnpl

_bup_urlopen = mnpl.urlopen

def setup():
	mnpl._log = False
	mnpl._out = StringIO()
	mnpl.urlopen = MagicMock(return_value = None)

def teardown():
	mnpl._out = None
	mnpl.urlopen = _bup_urlopen

def log_string() -> str:
	mnpl._out.seek(0, 0)
	return mnpl._out.read().strip()
