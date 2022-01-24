# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import mnpl

ENOCMD    = 1
EWRONGCMD = 2

_cmd = {}

def run(argv: list[str]):
	cmd = Path(argv[0]).stem.strip()
	if cmd == '':
		mnpl.error('empty command name')
		return ENOCMD
	mnpl.log('run', cmd)
	x = _cmd.get(cmd, None)
	if x is None:
		mnpl.error(f"{cmd}: invalid command")
		return EWRONGCMD
	return 0
