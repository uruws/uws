# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from subprocess import getstatusoutput

import uwscli

def check_storage():
	x = "df -kl %s" % uwscli.docker_storage
	x += " | tail -n1 | awk '{ print $4 }'"
	rc, out = getstatusoutput(x)
	if rc != 0:
		print(out, file = sys.stderr)
		return rc
	try:
		s = int(out)
	except ValueError:
		print('value error:', out, file = sys.stderr)
		return 9
	if s < uwscli.docker_storage_min:
		return 8
	return 0

def nq(app, version):
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

def cleanBuild(app, version):
	rc = uwscli.clean_build(app, version)
	if rc != 0:
		print('ERROR: app clean:', app, version, 'failed!', file = sys.stderr)

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.build_description())
	flags.add_argument('app', metavar = 'app', choices = uwscli.build_list(),
		default = 'app', help = 'app name')
	flags.add_argument('version', metavar = 'X.Y.Z', help = 'app version/tag')

	args = flags.parse_args(argv)

	rc = check_storage()
	if rc != 0:
		print('ERROR: not enough disk space!', file = sys.stderr)
		return rc

	rc = nq(args.app, args.version)
	if rc != 0:
		print("enqueue of %s build job failed!" % args.app, file = sys.stderr)
		return rc

	cleanBuild(args.app, args.version)

	print('')
	print('Check build job with:')
	print('  uwsq')
	print('')
	print('Deploy and check status with:')
	if args.app == 'app':
		print('')
		print("  Workers: app-deploy worker %s" % args.version)
		print('           app-status worker')
		print('')
		print("  Web: app-deploy app-(east|west) %s" % args.version)
		print('       app-status app-(east|west)')
	else:
		print('  app-deploy', args.app, args.version)
		print('  app-status', args.app)
	print('')
	print('Run uwshelp for more information.')

	return 0
