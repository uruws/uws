# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import uwscli

__doc__ = 'app reverse proxy logs'

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.app_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('-e', '--error', action = 'store_true', default = False,
		help = 'show error messages only')
	flags.add_argument('-f', '--follow', action = 'store_true', default = False,
		help = 'follow messages')
	flags.add_argument('-t', '--tail', type = int, default = 10,
		metavar = 'N', help = 'show last N messages (default 10)')
	flags.add_argument('-m', '--max', type = int, default = 0,
		metavar = 'N', help = 'max containers to get logs from')
	flags.add_argument('app', metavar = 'app', choices = uwscli.app_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	logs_args = "%s %s ngxlogs" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod)

	cmd = 'app-cmd.sh'
	ttl = uwscli.system_ttl
	if args.follow:
		cmd = 'app-cli.sh'
		ttl = 3600
		logs_args += ' --follow'

	if args.tail != 10:
		logs_args += " --tail=%d" % args.tail
	if args.max > 0:
		logs_args += " --max=%d" % args.max

	if args.error:
		logs_args += " --error"

	return uwscli.run(cmd, logs_args, timeout = ttl)
