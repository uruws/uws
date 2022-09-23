# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

def config() -> int:
	return 0

def report() -> int:
	return 0

def main(argv: list[str]) -> int:
	try:
		action = argv[0]
	except IndexError:
		action = 'report'
	if action == 'config':
		return config()
	return report()

if __name__ == '__main__': # pragma: no cover
	sys.exit(main(sys.argv[1:]))
