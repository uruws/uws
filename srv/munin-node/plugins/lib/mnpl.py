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

_log: bool   = getenv('UWS_LOG', 'on') == 'on'
_out: TextIO = stderr

def log(*args: Union[list[Any], Any]):
	if _log:
		print(*args, file = _out)

def error(*args: Union[list[Any], Any]):
	print('[E]', *args, file = _out)

_clusters_fn     = Path(getenv('UWS_CLUSTER_ENV', '/uws/etc/cluster.json'))
_clusters_domain = getenv('UWS_CLUSTER_DOMAIN', 'uws.talkingpts.org')

def clusters() -> list[dict[str, str]]:
	"""Returns clusters info."""
	k: list[dict[str, str]] = []
	with open(_clusters_fn, 'r') as fh:
		k = [d for d in json.load(fh) if d]
	return k

_tls_cert:    str  = getenv('UWS_TLS_CERT', '12a549fb-96a3-5131-aa15-9bc30cc7d99d')
_tls_conf:    Path = Path(getenv('UWS_TLS_CONF', '/uws/etc/ca/ops/client.pw'))
_tls_certdir: Path = Path(getenv('UWS_TLS_CERTDIR', '/uws/etc/ca/client'))

_ctx: Optional[SSLContext] = None

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

def _context() -> SSLContext:
	global _ctx
	if _ctx is None:
		certfn: Path = _tls_certdir.joinpath(f"{_tls_cert}.pem")
		keyfn:  Path = _tls_certdir.joinpath(f"{_tls_cert}-key.pem")
		pw:     str  = _getpw()
		_ctx = ssl.create_default_context()
		_ctx.load_cert_chain(
			certfile = certfn,
			keyfile  = keyfn,
			password = pw,
		)
	return _ctx

def _open(cluster: str, path: str, method: str, timeout: int) -> HTTPResponse:
	ctx = _context()
	req = Request(f"https://{cluster}.{_clusters_domain}{path}", method = method)
	return urlopen(req, timeout = timeout, context = ctx)

def GET(cluster: str, path: str, timeout: int = 7) -> HTTPResponse:
	return _open(cluster, path, 'GET', timeout)

@dataclass
class Config(object):
	path:   str = '/'
	status: int = 200

def main(argv: list[str], cfg: Config) -> int:
	rc = 0
	for k in clusters():
		try:
			resp = GET(k['host'], cfg.path)
			log(resp)
		except Exception as err:
			error(type(err), err, k)
			rc += 1
	return rc
