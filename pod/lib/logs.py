#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser
from os import system

def _system(cmd):
	return system(cmd) >> 8

def main(argv = []):
	flags = ArgumentParser(description = 'get pod logs')
	flags.add_argument('-c', '--container', metavar = 'name', default = '',
		help = 'pod container')
	flags.add_argument('-C', '--all-containers', action = 'store_true',
		default = False, help = 'all containers in the pod')
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

	args = flags.parse_args(argv)

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
		return _system(cmd)

	# all logs
	cmd += ' --prefix=true --ignore-errors'
	if args.max > 0:
		cmd += " --max-log-requests=%d" % args.max

	# label selector
	if args.label == '':
		cmd += " -l '*'"
	else:
		cmd += " -l %s" % args.label

	# pod container
	if args.container != '':
		cmd += " -c %s" % args.container
	elif args.all_containers is True:
		cmd += ' --all-containers=true'

	return _system(cmd)

if __name__ == '__main__': # pragma no cover
	sys.stdout.reconfigure(line_buffering = False) # type: ignore
	sys.stderr.reconfigure(line_buffering = False) # type: ignore
	sys.exit(main(sys.argv[1:]))
