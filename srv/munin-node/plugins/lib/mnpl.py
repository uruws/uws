# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

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

_cluster_env = Path(getenv('UWS_CLUSTER_ENV', '/uws/etc/cluster'))

def clusters() -> dict[str, Any]:
	"""Returns clusters info."""
	k: dict[str, Any] = {}
	return k

def GET(url: str, timeout: int = 7) -> HTTPResponse:
	return urlopen(f"https://{url}", timeout = timeout)
