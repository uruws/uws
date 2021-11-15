#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser

sys.path.insert(0, '/srv/home/uwscli/lib')
import uwscli

__doc__ = 'uws git deploy'

def main(argv = []):
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-r', '--repo', metavar = 'PATH', required = True,
		help = 'origin repo path')
	flags.add_argument('-t', '--tagref', metavar = 'git/tag/ref', required = True,
		help = 'pushed tag refname')

	args = flags.parse_args(argv)

	if not args.tagref.startswith('refs/tags/'):
		uwscli.error('[ERROR] not a tag reference:', args.tagref)
		return 1

	return 0

if __name__ == '__main__': # pragma: no coverage
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
