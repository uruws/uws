# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import mnpl

def run(argv: list[str]):
	cmd = Path(argv[0]).stem
	mnpl.log('run', cmd)
	return 0
