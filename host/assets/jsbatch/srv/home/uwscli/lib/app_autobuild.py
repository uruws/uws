# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import getenv
from pathlib import Path
from time import sleep

import uwscli
import app_build
import app_deploy

import semver # type: ignore

_status_dir = getenv('UWSCLI_BUILD_STATUS_DIR', '/run/uwscli/build')
_nqdir      = getenv('UWSCLI_NQDIR', '/run/uwscli/nq')

ESETUP  = 10
ETAG    = 11
EBUILD  = 12
EDEPLOY = 13

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
	st    = None
	ver   = None
	f     = Path(_status_dir, f"{app}.status")
	line  = f.read_text().strip()
	items = line.split(':')
	st    = items[0]
	ver   = items[1]
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

def _build(app: str) -> int:
	build = uwscli.app[app].build
	try:
		with uwscli.chdir(build.dir):
			rc = uwscli.run('app-fetch.sh', build.src)
			if rc != 0:
				return rc
			try:
				tag = _latestTag(build.src)
			except ValueError:
				uwscli.error('[ERROR] could not get latest git tag')
				return ETAG
			if _isBuildingOrDone(app, tag):
				return 0
			return app_build.run(app, tag)
	except SystemExit:
		pass
	return EBUILD

def _latestBuild(app):
	return str(max(filter(_semverFilter, uwscli.list_images(app))))

def _deploy(app: str, tag: str) -> int:
	t = semver.VersionInfo.parse(tag)
	ver: str = ''
	for n in uwscli.autobuild_deploy(app):
		if ver == '':
			ver = _latestBuild(n)
		if ver != '':
			v = semver.VersionInfo.parse(ver.split('-')[0])
			if v >= t:
				uwscli.info('app-build:', app, ver)
				rc = app_deploy.deploy(app, ver)
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
