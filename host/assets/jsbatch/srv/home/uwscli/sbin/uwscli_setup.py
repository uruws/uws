#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

__doc__ = 'setup uwscli environment'

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

_run = {
	0: 'uwscli_setup.sh',
}

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.deploy_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	args = flags.parse_args(argv)

	for i in sorted(_run.keys()):
		cmd = f"/srv/home/uwscli/sbin/{_run[i]}"
		rc = uwscli.system(cmd, env = {'PATH': '/bin:/usr/bin:/sbin:/usr/sbin'})
		if rc != 0:
			return rc

	return 0

if __name__ == '__main__':
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
