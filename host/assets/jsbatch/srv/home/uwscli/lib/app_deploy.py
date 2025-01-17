# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter

import uwscli
import custom_deploy

def deploy(app: str, version: str) -> int:
	uwscli.debug('deploy:', app, version)
	if not version in uwscli.list_images(app):
		uwscli.error("invalid %s build: %s" % (app, version))
		return 9
	args = "%s %s deploy %s" % (uwscli.app[app].cluster,
		uwscli.app[app].pod, version)
	return uwscli.ctl(args)

def wait(app: str) -> int:
	uwscli.debug('wait:', app)
	args = "%s %s wait" % (uwscli.app[app].cluster,
		uwscli.app[app].pod)
	return uwscli.ctl(args)

__doc__ = 'deploy app build'

def main(argv: list[str] = []) -> int:
	epilog = uwscli.deploy_description()
	epilog += '\nif no app version is provided a list of available builds will be shown'

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = epilog)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('-w', '--wait', action = 'store_true',
		default = False, help = 'wait for deployment to finish')
	flags.add_argument('-r', '--rollback', action = 'store_true',
		default = False, help = 'rollback to previous deployment if failed (implies --wait)')
	flags.add_argument('app', metavar = 'app', choices = uwscli.deploy_list(),
		default = 'app', help = 'app name')
	flags.add_argument('version', metavar = 'X.Y.Z-bpV', nargs = '?',
		default = '', help = 'app version including buildpack version too')

	args = flags.parse_args(argv)

	if args.version == '':
		return custom_deploy.show_builds(args.app)

	# --rollback implies --wait
	if args.rollback:
		args.wait = True

	rc = deploy(args.app, args.version)
	if rc != 0:
		uwscli.error("enqueue of %s deploy job failed!" % args.app)
		return rc
	# wait
	if args.wait:
		rc = wait(args.app)
		# rollback if failed
		if rc != 0 and args.rollback:
			uwscli.log('deploy failed, trying to rollback...')
			st = custom_deploy.rollback(args.app)
			if st != 0:
				uwscli.error('deploy rollback failed:', st)

	return rc
