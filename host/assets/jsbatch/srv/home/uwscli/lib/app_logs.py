# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.app_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('-f', '--follow', action = 'store_true', default = False,
		help = 'follow messages')
	flags.add_argument('-t', '--tail', type = int, default = 10,
		metavar = 'N', help = 'show last N messages (default 10)')
	flags.add_argument('-m', '--max', type = int, default = 0,
		metavar = 'N', help = 'max containers to get logs from')
	flags.add_argument('app', metavar = 'app', choices = uwscli.app_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	logs_args = "%s %s logs" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod)

	ttl = uwscli.system_ttl
	if args.follow:
		logs_args += ' -f'
		ttl = None

	if args.tail != 10:
		logs_args += " --tail=%d" % args.tail
	if args.max > 0:
		logs_args += " --max=%d" % args.max

	return uwscli.run('app-cli.sh', logs_args, timeout = ttl)
