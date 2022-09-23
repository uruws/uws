# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from io      import StringIO
from pathlib import Path

import mnpl_utils
import mnpl

bup_urlopen = mnpl.urlopen

bup_tls_cert = mnpl._tls_cert
bup_tls_conf = mnpl._tls_conf

bup_println = mnpl_utils.println
bup_time    = mnpl.time

def setup():
	mnpl_utils._log = False
	mnpl_utils._out = StringIO()
	mnpl.urlopen = MagicMock(return_value = None)
	mnpl_utils.println = MagicMock()
	mnpl.time = MagicMock(return_value = 1643392687.1620736)
	mnpl._ctx = None
	mnpl._ctx_auth = None
	mnpl._tls_cert = 'cert-id'
	mnpl._tls_conf = Path('~/test/data/client.pw').expanduser()

def teardown():
	mnpl_utils._out = None
	mnpl.urlopen = bup_urlopen
	mnpl_utils.println = bup_println
	mnpl._tls_cert = bup_tls_cert
	mnpl._tls_conf = bup_tls_conf

def log_string() -> str:
	mnpl_utils._out.seek(0, 0)
	return mnpl_utils._out.read().strip()
