# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

import mnpl

def main(argv: list[str]):
	cfg = mnpl.Config(
		path   = '/k8smon/_/ping',
	)
	return mnpl.main(argv, cfg)

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
