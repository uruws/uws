# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import inspect
import sys

from os import getenv

from typing import Any
# ~ from typing import Optional
from typing import TextIO
from typing import Union

_outfh: TextIO = sys.stdout
_errfh: TextIO = sys.stderr

# ~ from contextlib import contextmanager
# ~ from os import environ, getenv, getcwd, linesep
# ~ from os import chdir as os_chdir
# ~ from pathlib import Path
# ~ from subprocess import getstatusoutput, CalledProcessError
# ~ from subprocess import check_output as proc_check_output
# ~ from subprocess import run as proc_run

# ~ from uwscli_auth import User, getuser, user_auth

# ~ _user:  User = getuser()
_log:   bool = getenv('UWSCLI_LOG', 'on') == 'on'
_debug: bool = getenv('UWSCLI_DEBUG', 'off') == 'on'

def _print(*args: Union[list[Any], Any], fh = _outfh, sep = ' '):
	if _debug:
		s = inspect.stack()[2]
		print(f"{s.filename}:{s.function}:{s.lineno}:", *args,
			sep = sep, flush = True, file = fh)
	else:
		print(*args, sep = sep, flush = True, file = fh)

def log(*args: Union[list[Any], Any], sep: str = ' '):
	"""print log messages to stdout (can be disabled with UWSCLI_LOG=off env var)"""
	if _log:
		_print(*args, sep = sep, fh = _outfh)

def info(*args: Union[list[Any], Any]):
	"""print log messages to stdout (even if log is 'off')"""
	_print(*args, fh = _outfh)

def debug(*args: Union[list[Any], Any]):
	"""print debug messages to stdout"""
	if _debug:
		_print(*args, fh = _outfh)

def error(*args: Union[list[Any], Any]):
	"""print log messages to stderr"""
	_print(*args, fh = _errfh)
