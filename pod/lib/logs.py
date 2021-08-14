#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser
from os import system

def main():
	flags = ArgumentParser(description = 'get pod logs')
	flags.add_argument('-n', '--namespace', metavar = 'ns', required = True,
		help = 'pod namespace')
	flags.add_argument('-T', '--no-timestamps', action = 'store_true',
		default = False, help = 'do not show timestamps')
	flags.add_argument('-l', '--label', metavar = 'filter', default = '',
		help = 'filter label')
	flags.add_argument('-f', '--follow', action = 'store_true',
		default = False, help = 'follow messages')
	flags.add_argument('-t', '--tail', type = int, default = 10,
		metavar = 'N', help = 'show last N messages (default 10)')
	flags.add_argument('-m', '--max', type = int, default = 0,
		metavar = 'M', help = 'max pods')
	flags.add_argument('pod', metavar = 'name', nargs = '?',
		default = '', help = 'pod name')

	args = flags.parse_args()

	cmd = "uwskube logs"
	if not args.no_timestamps:
		cmd += " --timestamps"
	cmd += " -n %s" % args.namespace
	cmd += " --tail=%d" % args.tail
	if args.follow:
		cmd += ' -f'

	# pod logs
	if args.pod != '':
		cmd += " %s" % args.pod
		return system(cmd)

	# all logs
	cmd += ' --prefix=true --ignore-errors'
	if args.max > 0:
		cmd += " --max-log-requests=%d" % args.max
	if args.label == '':
		cmd += " -l '*'"
	else:
		cmd += " -l %s" % args.label
	return system(cmd)

if __name__ == '__main__':
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main())
