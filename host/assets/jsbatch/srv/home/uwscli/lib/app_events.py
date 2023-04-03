# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

__doc__ = 'show app cluster events'

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

	cmd = 'app-cmd.sh'
	ttl = uwscli.system_ttl
	if args.watch:
		cmd = 'app-cli.sh'
		ttl = 3600
		cmd_args += ' -w'

	return uwscli.run(cmd, cmd_args, timeout = ttl)
