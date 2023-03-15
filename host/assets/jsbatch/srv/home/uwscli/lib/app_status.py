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
	flags.add_argument('app', metavar = 'app', default = 'app',
		help = 'app name', choices = uwscli.deploy_list())

	args = flags.parse_args(argv)

	cmd_args = "%s %s status" % (uwscli.app[args.app].cluster,
		uwscli.app[args.app].pod)

	return uwscli.run('app-cmd.sh', cmd_args)
