# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import re
import ssl

from dataclasses import dataclass
from os          import getenv
from pathlib     import Path
from ssl         import SSLContext
from sys         import stderr
from sys         import stdout
from time        import time

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

def _print(*args: Union[list[Any], Any]):
	print(*args, file = stdout)

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

def _context(auth: bool) -> SSLContext:
	global _ctx
	if _ctx is None:
		_ctx = ssl.create_default_context()
	global _ctx_auth
	if auth and _ctx_auth is None:
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
	auth:     bool = True
	path:     str  = '/'
	status:   int  = 200
	timeout:  int  = 7
	label:    str  = 'number'
	base:     int  = 1000
	scale:    bool = True
	warning:  int  = 3
	critical: int  = 5

#
# http helpers
#

def _open(cluster: str, method: str, cfg: Config) -> HTTPResponse:
	ctx = _context(cfg.auth)
	req = Request(
		f"https://{cluster}.{_clusters_domain}{cfg.path}",
		method = method,
	)
	return urlopen(req, timeout = cfg.timeout, context = ctx)

def GET(cluster: str, cfg: Config) -> HTTPResponse:
	return _open(cluster, 'GET', cfg)

#
# main
#

def config(cfg: Config) -> int:
	for k in clusters():
		name = k['name']
		host = k['host']
		gid  = cleanfn(f"{name}_{cfg.path}_{cfg.status}")
		title = cfg.path
		if not cfg.auth:
			title += ' (no auth)'
			gid += '_no_auth'
		_print(f"multigraph k8s_{gid}")
		_print(f"graph_title k8s {name} {title}")
		_print(f"graph_args --base {cfg.base} -l 0")
		_print('graph_category', cleanfn(name))
		_print('graph_vlabel', cfg.label)
		if cfg.scale:
			_print('graph_scale yes')
		_print('a_latency.label latency seconds')
		_print('a_latency.colour COLOUR0')
		_print('a_latency.draw AREA')
		_print('a_latency.min 0')
		_print('a_latency.warning', cfg.warning)
		_print('a_latency.critical', cfg.critical)
		_print('a_latency.info', f"https://{host}.{_clusters_domain}{cfg.path}")
		_print('b_status.label status:', cfg.status)
		_print('b_status.colour COLOUR1')
		_print('b_status.draw LINE')
		_print('b_status.min 0')
		_print('b_status.max 1')
		_print('b_status.critical 1:')
	return 0

def _report(host: str, cfg: Config) -> tuple[float, float]:
	t: float = time()
	s: float = 0.0
	r: Union[HTTPResponse, HTTPError, None] = None
	try:
		r = GET(host, cfg)
	except HTTPError as err:
		r = err
	if r is not None:
		code: int = r.getcode()
		if code is not None and code == cfg.status:
			s = 1.0
	return (s, time() - t)

def report(cfg: Config) -> int:
	for k in clusters():
		name = k['name']
		host = k['host']
		gid  = cleanfn(f"{name}_{cfg.path}_{cfg.status}")
		if not cfg.auth:
			gid += '_no_auth'
		_print(f"multigraph k8s_{gid}")
		status, latency = _report(host, cfg)
		_print('a_latency.value', latency)
		_print('b_status.value', status)
	return 0

def main(argv: list[str], cfg: Config) -> int:
	try:
		action = argv[0]
	except IndexError:
		action = 'report'
	if action == 'config':
		return config(cfg)
	return report(cfg)
