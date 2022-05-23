#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

__doc__ = 'uwscli auth'

from argparse import ArgumentParser

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

import uwscli
import uwscli_log as log

from uwscli_auth import user_check

def main(argv = []):
	log.debug('run:', ' '.join(argv))
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-u', '--user', metavar = 'USER', required = True,
		help = 'uws user name')
	flags.add_argument('-b', '--build', metavar = 'APP',
		help = 'check build access', default = '')
	flags.add_argument('-p', '--pod', metavar = 'KIND',
		help = 'check pod access', default = '')
	flags.add_argument('-w', '--workdir', metavar = 'PATH',
		help = 'check access to app workdir', default = '')
	flags.add_argument('-o', '--ops', metavar = 'ACTION',
		help = 'check operator access', default = '')
	args = flags.parse_args(argv)
	return user_check(
		username = args.user,
		build    = args.build,
		pod      = args.pod,
		workdir  = args.workdir,
		ops      = args.ops,
	)

if __name__ == '__main__': # pragma: no coverage
	sys.exit(main(sys.argv[1:]))
