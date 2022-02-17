# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.app_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('-w', '--watch', action = 'store_true', default = False,
		help = 'watch for new messages')
	flags.add_argument('app', metavar = 'app', choices = uwscli.app_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	cmd_args = "%s %s events" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod)

	ttl = uwscli.system_ttl
	if args.watch:
		cmd_args += ' -w'
		ttl = None

	return uwscli.run('app-cli.sh', cmd_args, timeout = ttl)
