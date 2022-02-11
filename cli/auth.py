#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

__doc__ = 'uwscli auth'

from argparse import ArgumentParser

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

import uwscli

def main(argv = []):
	uwscli.debug('run')
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-u', '--user', metavar = 'USER', required = True,
		help = 'uws user name')
	flags.add_argument('-b', '--build', metavar = 'APP',
		help = 'check build access')
	flags.add_argument('-p', '--pod', metavar = 'KIND',
		help = 'check pod access')
	flags.add_argument('-w', '--workdir', metavar = 'PATH',
		help = 'check access to app workdir')
	args = flags.parse_args(argv)
	return 0

if __name__ == '__main__': # pragma: no coverage
	sys.exit(main(sys.argv[1:]))
