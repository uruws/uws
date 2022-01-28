# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from io      import StringIO
from pathlib import Path

import mnpl

bup_urlopen = mnpl.urlopen

bup_tls_cert = mnpl._tls_cert
bup_tls_conf = mnpl._tls_conf

bup_print = mnpl._print
bup_time  = mnpl.time

def setup():
	mnpl._log = False
	mnpl._out = StringIO()
	mnpl.urlopen = MagicMock(return_value = None)
	mnpl._print = MagicMock()
	mnpl.time = MagicMock(return_value = 1643392687.1620736)
	mnpl._ctx = None
	mnpl._ctx_auth = None
	mnpl._tls_cert = 'cert-id'
	mnpl._tls_conf = Path('~/test/data/client.pw').expanduser()

def teardown():
	mnpl._out = None
	mnpl.urlopen = bup_urlopen
	mnpl._print = bup_print
	mnpl._tls_cert = bup_tls_cert
	mnpl._tls_conf = bup_tls_conf

def log_string() -> str:
	mnpl._out.seek(0, 0)
	return mnpl._out.read().strip()
