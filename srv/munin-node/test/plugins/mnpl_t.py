# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from io import StringIO
import mnpl

mnpl._out = None

def setup():
	mnpl._log = False
	mnpl._out = StringIO()

def teardown():
	mnpl._out = None

def log_string() -> str:
	return mnpl._out.getvalue().strip()
