# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess
import sys

from os      import getenv
from pathlib import Path

#
# config
#

debug:       bool = getenv('UWS_WEBAPP_DEBUG', 'off') == 'on'
webapp_port: int  = int(getenv('UWS_WEBAPP_PORT', '2741'))
cmdpath:     Path = Path('/usr/bin/ab')

class Command(object):
	cmdargs:   list[str]
	timelimit: int       = 0

	def __init__(c, *args):
		c.cmdargs = args

	def args(c) -> list[str]:
		a = [cmdpath.as_posix()]
		a.extend(c.cmdargs)
		return a

def run(cmd: Command) -> int:
	timeout = 15
	if cmd.timelimit > 0:
		timeout = cmd.timelimit + 15
	try:
		proc = subprocess.run(cmd.args(), check = True, timeout = timeout,
			capture_output = True)
	except subprocess.CalledProcessError as err:
		return err.returncode
	except subprocess.TimeoutExpired:
		print('[ERROR] subprocess timeout:', cmd.args(), file = sys.stderr)
		return 1
	return 0
