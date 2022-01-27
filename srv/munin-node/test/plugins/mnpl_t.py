# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from io      import StringIO
from pathlib import Path

import mnpl

_bup_urlopen = mnpl.urlopen

_bup_tls_cert = mnpl._tls_cert
_bup_tls_conf = mnpl._tls_conf

def setup():
	mnpl._log = False
	mnpl._out = StringIO()
	mnpl.urlopen = MagicMock(return_value = None)
	mnpl._tls_cert = 'cert-id'
	mnpl._tls_conf = Path('~/test/data/client.pw').expanduser()

def teardown():
	mnpl._out = None
	mnpl.urlopen = _bup_urlopen
	mnpl._tls_cert = _bup_tls_cert
	mnpl._tls_conf = _bup_tls_conf

def log_string() -> str:
	mnpl._out.seek(0, 0)
	return mnpl._out.read().strip()
