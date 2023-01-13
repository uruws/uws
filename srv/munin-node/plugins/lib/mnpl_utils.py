# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import re
import ssl

from os      import getenv
from pathlib import Path
from ssl     import SSLContext
from sys     import stderr
from sys     import stdout

from http.client    import HTTPResponse
from urllib.error   import HTTPError
from urllib.request import Request
from urllib.request import urlopen

from typing import Any
from typing import Optional
from typing import TextIO
from typing import Union

#
# logger
#

_log: bool   = getenv('UWS_LOG', 'on') == 'on'
_out: TextIO = stderr

def log(*args: Union[list[Any], Any]):
	if _log:
		print(*args, file = _out)

def error(*args: Union[list[Any], Any]):
	print('[E]', *args, file = _out)

#
# utils
#

__field_re = re.compile('\W')

def cleanfn(n):
	return __field_re.sub('_', n)

def println(*args: Union[list[Any], Any]):
	print(*args, file = stdout)

#
# tls setup
#

_tls_cert:    str  =      getenv('UWS_TLS_CERT',    '12a549fb-96a3-5131-aa15-9bc30cc7d99d')
_tls_conf:    Path = Path(getenv('UWS_TLS_CONF',    '/uws/etc/ca/ops/client.pw'))
_tls_certdir: Path = Path(getenv('UWS_TLS_CERTDIR', '/uws/etc/ca/client'))

_ctx:      Optional[SSLContext] = None
_ctx_auth: Optional[SSLContext] = None

def _tls_getpw() -> str:
	pw: str  = ''
	with open(_tls_conf, 'r') as fh:
		for line in fh.readlines():
			field = line.strip().split(':')
			try:
				if field[0] == _tls_cert:
					return field[1]
			except IndexError:
				pass
	return pw

def _tls_context(auth: bool) -> Optional[SSLContext]:
	global _ctx
	if _ctx is None:
		_ctx = ssl.create_default_context()
	global _ctx_auth
	if auth and _ctx_auth is None:
		certfn: Path = _tls_certdir.joinpath(f"{_tls_cert}.pem")
		keyfn:  Path = _tls_certdir.joinpath(f"{_tls_cert}-key.pem")
		pw:     str  = _tls_getpw()
		_ctx_auth = ssl.create_default_context()
		_ctx_auth.load_cert_chain(
			certfile = certfn,
			keyfile  = keyfn,
			password = pw,
		)
	if auth:
		return _ctx_auth
	return _ctx

#
# http helpers
#

def GET(url: str, timeout: int = 7, auth: bool = True) -> HTTPResponse:
	ctx = _tls_context(auth)
	req = Request(url, method = 'GET')
	return urlopen(req, timeout = timeout, context = ctx)
