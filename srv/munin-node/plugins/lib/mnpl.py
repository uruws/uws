# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from os      import getenv
from pathlib import Path
from sys     import stderr

from http.client    import HTTPResponse
from urllib.request import urlopen

from typing import Any
from typing import TextIO

_log: bool   = getenv('UWS_LOG', 'on') == 'on'
_out: TextIO = stderr

def log(*args: list[Any]):
	if _log:
		print(*args, file = _out)

def error(*args: list[Any]):
	print('[E]', *args, file = _out)

_clusters_fn = Path(getenv('UWS_CLUSTER_ENV', '/uws/etc/cluster.json'))

def clusters() -> list[dict[str, str]]:
	"""Returns clusters info."""
	k: list[dict[str, str]] = []
	with open(_clusters_fn, 'r') as fh:
		k = [d for d in json.load(fh) if d]
	return k

def GET(url: str, timeout: int = 7) -> HTTPResponse:
	return urlopen(f"https://{url}", timeout = timeout)
