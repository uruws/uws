#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

__doc__ = 'uwsapp users auth'

from argparse import ArgumentParser
from uuid     import uuid5
from uuid     import NAMESPACE_DNS

import uwscli

def main(argv: list[str] = []) -> int:
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	args = flags.parse_args(argv)

	for user in uwscli.user_list():
		username = user.username.strip()
		if username != '':
			uid = uuid5(NAMESPACE_DNS, username)
			rc = uwscli.system('/usr/bin/install -v -d -m 0750 -u uws -g uws /run/uwscli/auth/%s' % uid)

	return 0

if __name__ == '__main__': # pragma: no cover
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
