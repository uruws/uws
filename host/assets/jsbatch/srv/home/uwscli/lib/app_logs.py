# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.app_description())
	flags.add_argument('-f', '--follow', action = 'store_true', default = False,
		help = 'follow messages')
	flags.add_argument('-t', '--tail', type = int, default = 10,
		metavar = 'N', help = 'show last N messages (default 10)')
	flags.add_argument('app', metavar = 'app', choices = uwscli.app_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	logs_args = "%s %s logs" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod)

	if args.follow:
		logs_args += ' -f'
	if args.tail != 10:
		logs_args += " --tail=%d" % args.tail

	return uwscli.run('app-cli.sh', logs_args)
