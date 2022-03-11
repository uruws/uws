# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import getenv
from pathlib import Path

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
	uwscli.debug('setup')
	try:
		uwscli.mkdir(_status_dir)
		uwscli.mkdir(_nqdir)
	except Exception as err:
		uwscli.error(err)
		return False
	return True

def _latestTag(src):
	uwscli.debug('latestTag')
	vmax = None
	for t in uwscli.git_tag_list(workdir = src):
		try:
			v = semver.VersionInfo.parse(t)
		except ValueError as err:
			uwscli.debug('latest tag semver error:', err)
			continue
		if vmax is None:
			vmax = v
		else:
			if v > vmax:
				vmax = v
	return str(vmax)

def _getStatus(app):
	uwscli.debug('getStatus')
	st    = None
	ver   = None
	f     = Path(_status_dir, f"{app}.status")
	line  = f.read_text().strip()
	items = line.split(':')
	st    = items[0]
	ver   = items[1]
	return (st, ver)

def _checkVersion(tag: str, ver: str) -> bool:
	"""check if tag is major than version"""
	uwscli.debug('checkVersion')
	t = semver.VersionInfo.parse(tag)
	v = semver.VersionInfo.parse(ver)
	return t > v

def _isBuildingOrDone(app, tag):
	"""check if tag is in the build queue or done already"""
	uwscli.debug(app, tag)
	try:
		st, ver = _getStatus(app)
		not_done = _checkVersion(tag, ver)
		if not_done:
			uwscli.debug('not done:', app, tag)
			return False
	except FileNotFoundError:
		uwscli.debug('no status:', app, tag)
		return False
	ok = st != 'FAIL'
	if ok:
		uwscli.debug('already built app:', app, tag)
	else:
		uwscli.error('build for app:', app, ver, 'failed')
	return True

__done: str = '__done__'

def _build(app: str) -> tuple[int, str]:
	build = uwscli.app[app].build
	uwscli.debug(build)
	try:
		with uwscli.chdir(build.dir):
			uwscli.debug('build.dir:', build.dir)
			rc = uwscli.run('app-fetch.sh', build.src)
			if rc != 0:
				uwscli.error('[ERROR] app-fetch.sh failed, exit status:', rc)
				return (rc, '')
			tag = _latestTag(build.src)
			if tag == 'None':
				uwscli.error('[ERROR] could not get latest git tag')
				return (ETAG, '')
			if _isBuildingOrDone(app, tag):
				return (0, __done)
			return (app_build.run(app, tag), tag)
	except SystemExit:
		pass
	return (EBUILD, '')

def _latestBuild(app: str) -> str:
	uwscli.debug('latestBuild')
	l = None
	for img in uwscli.list_images(app):
		try:
			v = semver.VersionInfo.parse(img)
		except ValueError as err:
			uwscli.debug('latest build semver error:', err)
			continue
		if l is None:
			l = v
		else:
			if v > l:
				l = v
	return str(l)

def _deploy(app: str, tag: str) -> int:
	uwscli.debug('deploy:', app, tag)
	t = semver.VersionInfo.parse(tag)
	ver: str = ''
	for n in uwscli.autobuild_deploy(app):
		uwscli.debug('deploy:', n)
		if ver == '':
			uwscli.debug('get', app, 'latest build')
			ver = _latestBuild(n)
		if ver != '':
			uwscli.debug('version:', ver)
			v = semver.VersionInfo.parse(ver.split('-')[0])
			if v >= t:
				uwscli.debug('new version to deploy:', ver)
				uwscli.info('app-deploy:', n, ver)
				rc = app_deploy.deploy(n, ver)
				if rc != 0:
					return EDEPLOY
			else:
				uwscli.info('nothing to do for app:', n, '- ver:', ver, '- tag:', tag)
		else:
			uwscli.info('no build to deploy for app:', n)
	return 0

def main(argv = []):
	uwscli.debug('main')

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.autobuild_description())

	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	flags.add_argument('app', metavar = 'app', choices = uwscli.autobuild_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	if not _setup():
		return ESETUP

	rc, tag = _build(args.app)
	if rc != 0:
		return rc

	if tag is __done:
		return 0

	return _deploy(args.app, tag)
