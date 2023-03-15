# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

__doc__ = 'scale app'

def main(argv: list[str] = []) -> int:
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.deploy_description())
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('app', metavar = 'app', default = 'app',
		help = 'app name', choices = uwscli.deploy_list())
	flags.add_argument('replicas', metavar = 'N', type = int,
		help = 'number of replicas')

	args = flags.parse_args(argv)

	if args.replicas <= 0:
		uwscli.error('invalid number of replicas:', args.replicas)
		return 9

	cmd_args = "%s %s scale %d" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod, args.replicas)

	return uwscli.ctl(cmd_args)
