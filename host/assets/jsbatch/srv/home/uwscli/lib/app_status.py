# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

__doc__ = 'show app deploy status'

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.deploy_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('-w', '--watch', action = 'store_true', default = False,
		help = 'watch pod status changes')
	flags.add_argument('-T', '--timeout', type = int, default = 3600,
		help = 'watch timeout seconds')
	flags.add_argument('app', metavar = 'app', default = 'app',
		help = 'app name', choices = uwscli.deploy_list())

	args = flags.parse_args(argv)

	if args.watch is True:
		cmd_args = "%s %s watch" % (uwscli.app[args.app].cluster,
			uwscli.app[args.app].pod)
		return uwscli.run('app-cli.sh', cmd_args, timeout = args.timeout)

	cmd_args = "%s %s status" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod)
	return uwscli.run('app-cmd.sh', cmd_args)
