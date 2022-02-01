# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from time import sleep

import uwscli

def run(app: str, version: str, timeout: int = 3600) -> int:
	st = check_storage()
	if st != 0:
		return st
	st = _build(app, version, timeout = timeout)
	if st != 0:
		return st
	sleep(1)
	cleanBuild(app, version)
	return 0

def check_storage() -> int:
	x = "df -kl %s" % uwscli.docker_storage
	x += " | tail -n1 | awk '{ print $4 }'"
	rc, out = uwscli.gso(x)
	if rc != 0:
		uwscli.error(out)
		return rc
	try:
		s = int(out)
	except ValueError:
		uwscli.error('value error:', out)
		return 9
	if s < uwscli.docker_storage_min:
		return 8
	return 0

def _build(app: str, version: str, timeout: int = 3600) -> int:
	builder = uwscli.app[app].build.type
	build_dir = uwscli.app[app].build.dir
	build_script = uwscli.app[app].build.script
	if builder == 'pack':
		src = uwscli.app[app].build.src
		target = uwscli.app[app].build.target
		args = "--src %s --target %s --version %s" % (src, target, version)
		return uwscli.run(build_script, args, cmddir = build_dir, timeout = timeout)
	else:
		args = "%s %s %s %s" % (app, build_dir, build_script, version)
		return uwscli.run('app-build.sh', args, timeout = timeout)

def nq(app: str, version: str):
	builder = uwscli.app[app].build.type
	build_dir = uwscli.app[app].build.dir
	build_script = uwscli.app[app].build.script
	if builder == 'pack':
		src = uwscli.app[app].build.src
		target = uwscli.app[app].build.target
		args = "--src %s --target %s --version %s" % (src, target, version)
		return uwscli.nq(build_script, args, build_dir)
	else:
		args = "%s %s %s %s" % (app, build_dir, build_script, version)
		return uwscli.nq('app-build.sh', args)

def cleanBuild(app: str, version: str):
	rc = uwscli.clean_build(app, version)
	if rc != 0:
		uwscli.error('ERROR: app clean:', app, version, 'failed!')

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.build_description())
	flags.add_argument('app', metavar = 'app', choices = uwscli.build_list(),
		default = 'app', help = 'app name')
	flags.add_argument('version', metavar = 'X.Y.Z', help = 'app version/tag')

	args = flags.parse_args(argv)

	rc = check_storage()
	if rc != 0:
		uwscli.error('ERROR: not enough disk space!')
		return rc

	rc = nq(args.app, args.version)
	if rc != 0:
		uwscli.error("enqueue of %s build job failed!" % args.app)
		return rc

	cleanBuild(args.app, args.version)

	uwscli.log('')
	uwscli.log('Check build job with:')
	uwscli.log('  uwsq')
	uwscli.log('')
	uwscli.log('Deploy and check status with:')
	if args.app == 'app':
		uwscli.log('')
		uwscli.log("  Workers: app-deploy worker %s" % args.version)
		uwscli.log('           app-status worker')
		uwscli.log('')
		uwscli.log("  Web: app-deploy app-(east|west) %s" % args.version)
		uwscli.log('       app-status app-(east|west)')
	else:
		uwscli.log('  app-deploy', args.app, args.version)
		uwscli.log('  app-status', args.app)
	uwscli.log('')
	uwscli.log('Run uwshelp for more information.')

	return 0
