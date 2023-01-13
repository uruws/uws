# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

from io           import StringIO
from pathlib      import Path
from urllib.error import URLError

import mnpl_utils
import mnpl

bup_urlopen = mnpl_utils.urlopen

bup_tls_cert = mnpl_utils._tls_cert
bup_tls_conf = mnpl_utils._tls_conf

bup_println = mnpl_utils.println
bup_time    = mnpl.time

def setup():
	mnpl_utils._log = False
	mnpl_utils._out = StringIO()
	mnpl_utils.urlopen = MagicMock(return_value = None)
	mnpl_utils.println = MagicMock()
	mnpl.time = MagicMock(return_value = 1643392687.1620736)
	mnpl_utils._ctx = None
	mnpl_utils._ctx_auth = None
	mnpl_utils._tls_cert = 'cert-id'
	mnpl_utils._tls_conf = Path('~/test/data/client.pw').expanduser()

def teardown():
	mnpl_utils._out = None
	mnpl.urlopen = bup_urlopen
	mnpl_utils.println = bup_println
	mnpl._tls_cert = bup_tls_cert
	mnpl._tls_conf = bup_tls_conf

def log_string() -> str:
	mnpl_utils._out.seek(0, 0)
	return mnpl_utils._out.read().strip()

def http_response_mock(code = 200, body = ''):
	r = MagicMock()
	r.code = code
	r.getcode = MagicMock(return_value = code)
	# ~ def _read(*args, **kwargs):
		# ~ return body.encode()
	# ~ r.read = MagicMock(side_effect = _read)
	def _readlines(*args, **kwargs):
		return body.encode().splitlines()
	r.readlines = MagicMock(side_effect = _readlines)
	return r

@contextmanager
def mock_utils_GET(resp = None, timeout_error = False, code = 200, body = ''):
	bup = mnpl_utils.GET
	if resp is None:
		resp = http_response_mock(code = code, body = body)
	def _timeout_error(*args, **kwargs):
		raise URLError('mock_utils_GET_timeout_error')
	try:
		if timeout_error:
			mnpl_utils.GET = MagicMock(side_effect = _timeout_error)
		else:
			mnpl_utils.GET = MagicMock(return_value = resp)
		yield resp
	finally:
		mnpl_utils.GET = bup
