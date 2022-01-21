# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from io import StringIO
import mnpl

mnpl._log = False
mnpl._out = StringIO()

def setup():
	mnpl._log = False

def teardown():
	mnpl._out.flush()

def log_string() -> str:
	return mnpl._out.getvalue().strip()
