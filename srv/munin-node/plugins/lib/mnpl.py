# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from io import TextIOWrapper
from os import getenv
from sys import stderr

from typing import Any

_log: bool = getenv('UWS_LOG', 'on') == 'on'
_out: TextIOWrapper = stderr

def log(*args: list[Any]):
	if _log:
		print(*args, file = _out)
