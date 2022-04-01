#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

__doc__ = 'setup uwscli environment'

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

class _cmdFailed(Exception):
	rc = -1

	def __init__(self, rc):
		super().__init__()
		self.rc = rc

def _run(cmd, args: list[str] = []):
	uwscli.log('***', cmd)
	x = f"/srv/home/uwscli/sbin/{cmd}"
	if len(args) > 0:
		x = f"{x} {' '.join(args)}"
	rc = uwscli.system(x, env = {'PATH': '/bin:/usr/bin:/sbin:/usr/sbin'})
	if rc != 0:
		uwscli.error(f"{cmd}: exit status {rc}")
		raise _cmdFailed(rc)

def _getUsers() -> list[str]:
	l = []
	return l

def main(argv: list[str] = []) -> int:
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.deploy_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	args = flags.parse_args(argv)

	try:
		_run('uwscli_setup.sh')
		_run('uwscli_user_profile.sh', _getUsers())
	except _cmdFailed as err:
		return err.rc

	return 0

if __name__ == '__main__': # pragma: no cover
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
