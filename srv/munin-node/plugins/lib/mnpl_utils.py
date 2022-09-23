# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import re

from os  import getenv
from sys import stderr
from sys import stdout

from typing import Any
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
