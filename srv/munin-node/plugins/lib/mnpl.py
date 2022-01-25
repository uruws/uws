# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http.client import HTTPResponse

from os     import getenv
from sys    import stderr
from typing import Any
from typing import AnyStr
from typing import TextIO

from urllib.request import urlopen

_log: bool   = getenv('UWS_LOG', 'on') == 'on'
_out: TextIO = stderr

def log(*args: list[Any]):
	if _log:
		print(*args, file = _out)

def error(*args: list[Any]):
	print('[E]', *args, file = _out)

def GET(url: str, timeout: int = 7) -> HTTPResponse:
	return urlopen(f"https://{url}", timeout = timeout)
