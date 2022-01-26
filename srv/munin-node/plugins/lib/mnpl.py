# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import ssl

from dataclasses import dataclass
from os          import getenv
from pathlib     import Path
from ssl         import SSLContext
from sys         import stderr

from http.client    import HTTPResponse
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
# clusters config
#

_clusters_fn     = Path(getenv('UWS_CLUSTER_ENV', '/uws/etc/cluster.json'))
_clusters_domain = getenv('UWS_CLUSTER_DOMAIN', 'uws.talkingpts.org')

def clusters() -> list[dict[str, str]]:
	"""Returns clusters info."""
	k: list[dict[str, str]] = []
	with open(_clusters_fn, 'r') as fh:
		k = [d for d in json.load(fh) if d]
	return k

#
# tls setup
#

_tls_cert:    str  = getenv('UWS_TLS_CERT', '12a549fb-96a3-5131-aa15-9bc30cc7d99d')
_tls_conf:    Path = Path(getenv('UWS_TLS_CONF', '/uws/etc/ca/ops/client.pw'))
_tls_certdir: Path = Path(getenv('UWS_TLS_CERTDIR', '/uws/etc/ca/client'))

_ctx:      Optional[SSLContext] = None
_ctx_auth: Optional[SSLContext] = None

def _getpw() -> str:
	pw: str  = 'None'
	with open(_tls_conf, 'r') as fh:
		for line in fh.readlines():
			field = line.strip().split(':')
			try:
				if field[0] == _tls_cert:
					return field[1]
			except IndexError:
				pass
	return pw

def _context(auth: bool) -> SSLContext:
	global _ctx
	if _ctx is None:
		_ctx = ssl.create_default_context()
	global _ctx_auth
	if _ctx_auth is None:
		certfn: Path = _tls_certdir.joinpath(f"{_tls_cert}.pem")
		keyfn:  Path = _tls_certdir.joinpath(f"{_tls_cert}-key.pem")
		pw:     str  = _getpw()
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
# plugin config
#

@dataclass
class Config(object):
	auth:    bool = True
	path:    str  = '/'
	status:  int  = 200
	timeout: int  = 7

#
# http helpers
#

def _open(cluster: str, method: str, cfg: Config) -> HTTPResponse:
	ctx = _context(cfg.auth)
	req = Request(f"https://{cluster}.{_clusters_domain}{cfg.path}", method = method)
	return urlopen(req, timeout = cfg.timeout, context = ctx)

def GET(cluster: str, cfg: Config) -> HTTPResponse:
	return _open(cluster, 'GET', cfg)

# main

def main(argv: list[str], cfg: Config) -> int:
	rc = 0
	for k in clusters():
		try:
			resp = GET(k['host'], cfg)
			log(resp)
		except Exception as err:
			error(type(err), err, k)
			rc += 1
	return rc
