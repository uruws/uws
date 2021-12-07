# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import getenv
from pathlib import Path
from time import sleep

import uwscli

import semver

_status_dir = getenv('UWSCLI_BUILD_STATUS_DIR', '/run/uwscli/build')
_nqdir = getenv('UWSCLI_NQDIR', '/run/uwscli/nq')

ESETUP     = 10
ETAG       = 11
EBUILD_RUN = 12
EDEPLOY_NQ = 13
EBUILD     = 14
EDEPLOY    = 15

def _setup():
	try:
		uwscli.mkdir(_status_dir)
		uwscli.mkdir(_nqdir)
	except Exception as err:
		uwscli.error(err)
		return False
	return True

def _semverFilter(s):
	try:
		return semver.VersionInfo.parse(s)
	except ValueError:
		return None

def _latestTag(src):
	# https://python-semver.readthedocs.io/en/2.13.0/usage.html
	return str(max(filter(_semverFilter, uwscli.git_tag_list(workdir = src))))

def _getStatus(app):
	st = None
	ver = None
	f = Path(_status_dir, f"{app}.status")
	line = f.read_text().strip()
	items = line.split(':')
	st = items[0]
	ver = items[1]
	return (st, ver)

def _checkVersion(tag, ver):
	"""check if tag is major than version"""
	t = semver.VersionInfo.parse(tag)
	v = semver.VersionInfo.parse(ver)
	if t > v:
		return True
	return False

def _isBuildingOrDone(app, tag):
	"""check if tag is in the build queue or done already"""
	try:
		__, ver = _getStatus(app)
		build_ver = _checkVersion(tag, ver)
		if build_ver:
			return False
	except FileNotFoundError:
		return False
	return True

def _dispatch(app, tag):
	"""dispatch app tag build"""
	cmd = f"/srv/home/uwscli/bin/app-build {app} {tag}"
	rc = uwscli.system(cmd)
	if rc != 0:
		return EBUILD_RUN
	sleep(1)
	x = [
		'/usr/bin/nq',
		'-c',
		'--',
		'/srv/home/uwscli/bin/app-autobuild',
		app,
		'--deploy',
		tag,
	]
	rc = uwscli.system(' '.join(x), env = {'NQDIR': _nqdir})
	if rc != 0:
		return EDEPLOY_NQ
	return 0

def _build(app):
	build = uwscli.app[app].build
	try:
		with uwscli.chdir(build.dir):
			rc = uwscli.git_fetch(workdir = build.src)
			if rc != 0:
				return rc
			try:
				tag = _latestTag(build.src)
			except ValueError:
				uwscli.error('[ERROR] could not get latest git tag')
				return ETAG
			if _isBuildingOrDone(app, tag):
				return 0
			return _dispatch(app, tag)
	except SystemExit:
		pass
	return EBUILD

def _latestBuild(app):
	return str(max(filter(_semverFilter, uwscli.list_images(app))))

def _deploy(app, tag):
	ver = _latestBuild(app)
	t = semver.VersionInfo.parse(tag)
	v = semver.VersionInfo.parse(ver.split('-')[0])
	if v >= t:
		for n in uwscli.autobuild_deploy(app):
			uwscli.log(app, 'autobuild deploy:', n, ver)
			cmd = f"/srv/home/uwscli/bin/app-deploy {n} {ver}"
			rc = uwscli.system(cmd)
			if rc != 0:
				return EDEPLOY
	return 0

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.autobuild_description())

	deploy_tag = False
	if '--deploy' in argv:
		flags.add_argument('--deploy', metavar = 'TAG', default = '',
			help = 'app deploy stage')
		deploy_tag = True

	flags.add_argument('app', metavar = 'app', choices = uwscli.autobuild_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	if not _setup():
		return ESETUP

	if deploy_tag:
		return _deploy(args.app, args.deploy)

	return _build(args.app)
