# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import mnpl

def run(argv: list[str]):
	cmd = Path(argv[0]).stem.strip()
	if cmd == '':
		mnpl.error('empty command name')
		return 1
	mnpl.log('run', cmd)
	return 0
