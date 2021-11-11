# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli

def deploy(app, version):
	args = "%s %s deploy %s" % (uwscli.app[app].cluster,
		uwscli.app[app].pod, version)
	return uwscli.ctl(args)

def main(argv = []):
	epilog = uwscli.deploy_description()
	epilog += '\nif no app version is provided a list of available builds will be shown'

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = epilog)
	flags.add_argument('app', metavar = 'app', choices = uwscli.deploy_list(),
		default = 'app', help = 'app name')
	flags.add_argument('version', metavar = 'X.Y.Z-bpV', nargs = '?',
		default = '', help = 'app version including buildpack version too')

	args = flags.parse_args(argv)

	if args.version != '':
		if not args.version in uwscli.list_images(args.app):
			uwscli.error("invalid %s build: %s" % (args.app, args.version))
			return 1
		rc = deploy(args.app, args.version)
		if rc != 0:
			uwscli.error("enqueue of %s deploy job failed!" % args.app)
			return rc
	else:
		images = uwscli.list_images(args.app)
		if len(images) > 0:
			uwscli.log('available', args.app, 'builds:')
			for n in images:
				uwscli.log(' ', n)
		else:
			uwscli.log('no available builds for', args.app)

	return 0
