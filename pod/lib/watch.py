#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser
from os import system

def _system(cmd):
	return system(cmd) >> 8

def main(argv = []):
	flags = ArgumentParser(description = 'watch pod status')
	flags.add_argument('-n', '--namespace', metavar = 'ns', required = True,
		help = 'pod namespace')

	args = flags.parse_args(argv)

	cmd = f"uwskube get pod --watch -n {args.namespace} | ./pod/lib/timestamps.py"
	return _system(cmd)

if __name__ == '__main__': # pragma no cover
	sys.stdout.reconfigure(line_buffering = False) # type: ignore
	sys.stderr.reconfigure(line_buffering = False) # type: ignore
	sys.exit(main(sys.argv[1:]))
