#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser
from os       import system

def _system(cmd):
	return system(cmd) >> 8

def main(argv = []):
	flags = ArgumentParser(description = 'haproxy access logs')
	flags.add_argument('-e', '--error', action = 'store_true',
		default = False, help = 'show error messages only')
	flags.add_argument('-f', '--follow', action = 'store_true',
		default = False, help = 'follow messages')
	flags.add_argument('-q', '--quiet', action = 'store_true',
		default = False, help = 'reduce verbosity')
	flags.add_argument('-t', '--tail', type = int, default = 10,
		metavar = 'N', help = 'show last N messages (default 10)')
	flags.add_argument('-m', '--max', type = int, default = 0,
		metavar = 'M', help = 'max pods')
	flags.add_argument('pod', metavar = 'name',
		default = '', help = 'pod name')

	args = flags.parse_args(argv)

	cmd = "./pod/%s/hpx/access-logs.sh" % args.pod
	cmd += " --tail=%d" % args.tail

	if args.follow:
		cmd += ' -f'
	if args.max > 0:
		cmd += " --max=%d" % args.max

	cmd += " | /usr/local/bin/hpxlogs"
	if args.error:
		cmd += " -error"
	if args.quiet:
		cmd += ' -quiet'

	return _system(cmd)

if __name__ == '__main__': # pragma no cover
	sys.stdout.reconfigure(line_buffering = False) # type: ignore
	sys.stderr.reconfigure(line_buffering = False) # type: ignore
	sys.exit(main(sys.argv[1:]))
