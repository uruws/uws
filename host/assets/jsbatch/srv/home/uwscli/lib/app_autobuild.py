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

#
# filesystem setup
#

def _setup():
	uwscli.debug('setup')
	try:
		uwscli.mkdir(_status_dir)
		uwscli.mkdir(_nqdir)
	except Exception as err:
		uwscli.error(err)
		return False
	return True

#
# autobuild
#

def _ignoreTag(app: str, tag: str) -> bool:
	# CS: build 1.x tags only
	if app.startswith('cs') and not tag.startswith('1.'):
		uwscli.debug('tag ignore:', app, 'tag', tag)
		return True
	# App: build 2.x tags only
	elif app.startswith('app') and not tag.startswith('2.'):
		uwscli.debug('tag ignore:', app, 'tag', tag)
		return True
	# app build version blacklist
	elif uwscli.build_blacklist(app, tag):
		uwscli.debug('tag blacklist:', app, 'tag', tag)
		return True
	# ~ uwscli.debug('tag not blacklisted:', app, 'tag', tag)
	return False

def _latestTag(app: str, src: str) -> str:
	uwscli.debug('latestTag:', app, src)
	vmax = None
	for t in uwscli.git_tag_list(workdir = src):
		if _ignoreTag(app, t):
			continue
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
	uwscli.debug('latestTag:', app, src, str(vmax))
	if vmax is None:
		return ''
	return str(vmax)

def _getStatus(app: str) -> tuple[str, str]:
	if app == 'cs': app = 'crowdsourcing'
	uwscli.debug('getStatus:', app)
	st    = None
	ver   = None
	f     = Path(_status_dir, f"{app}.status")
	line  = f.read_text().strip()
	items = line.split(':')
	st    = items[0].strip().upper()
	ver   = items[1].strip()
	uwscli.debug('getStatus:', app, st, ver)
	return (st, ver)

def _checkVersion(tag: str, ver: str) -> bool:
	"""check if tag is major than version"""
	uwscli.debug('checkVersion:', tag, ver)
	t = semver.VersionInfo.parse(tag)
	v = semver.VersionInfo.parse(ver)
	if t > v:
		uwscli.log('tag', tag, 'is newer than latest build', ver)
		return True
	uwscli.debug('tag', tag, 'is older than or equal to the latest build', ver)
	return False

def _isBuildingOrDone(app: str, tag: str) -> bool:
	"""check if tag is in the build queue or done already"""
	uwscli.debug('isBuildingOrDone:', app, tag)
	st = ''
	ver = ''
	# no status file
	try:
		st, ver = _getStatus(app)
	except FileNotFoundError:
		uwscli.debug('no status file:', app, tag)
	# already done?
	if uwscli.build_done(app, tag):
		uwscli.debug('already built:', app, tag)
		return True
	if st == '':
		uwscli.log('no status:', app, tag)
		return False
	# check status version
	not_done = _checkVersion(tag, ver)
	if not_done:
		uwscli.log('not done:', app, tag)
		return False
	# app is being built
	if st == 'BUILD':
		uwscli.log('building:', app, ver)
		return True
	# previous build failed
	ok = st != 'FAIL'
	if ok:
		uwscli.debug('done already:', app, tag)
	else:
		# alert about it but consider it done
		uwscli.error('[ERROR] build failed:', app, ver)
	return True

def _build(app: str, dryrun: bool = False) -> int:
	build = uwscli.app[app].build
	uwscli.debug(app, build)
	try:
		with uwscli.chdir(build.dir):
			uwscli.debug('build.dir:', build.dir)
			rc = 0
			rc = uwscli.run('app-fetch.sh', build.src)
			if rc != 0:
				uwscli.error('[ERROR] app-fetch.sh failed, exit status:', rc)
				return rc
			tag = _latestTag(app, build.src)
			if tag == '':
				uwscli.error('[ERROR] could not get latest git tag')
				return ETAG
			if _isBuildingOrDone(app, tag):
				return 0
			uwscli.log('dispatch autobuild:', app, tag)
			if dryrun:
				uwscli.log('dry run enabled, autobuild aborted!')
				return 0
			return app_build.run(app, tag)
	except SystemExit:
		pass
	return EBUILD

#
# autodeploy
#

def _latestBuild(app: str, tag: str = '') -> str:
	uwscli.debug('latestBuild:', app, tag)
	l = None
	for img in uwscli.list_images(app):
		try:
			v = semver.VersionInfo.parse(img)
		except ValueError as err:
			uwscli.debug('latest build semver error:', err)
			continue
		if tag != '' and not str(v).startswith(tag):
			continue
		if _ignoreTag(app, str(v)):
			continue
		if l is None:
			l = v
		else:
			if v > l:
				l = v
	if l is None:
		return ''
	return str(l)

def _deploy(app: str, tag: str) -> int:
	uwscli.debug('deploy:', app, tag)
	t = semver.VersionInfo.parse(tag)
	ver: str = ''
	for n in uwscli.autobuild_deploy(app):
		uwscli.debug('deploy:', n)
		if ver == '':
			uwscli.debug('get', app, 'latest build')
			ver = _latestBuild(n, tag = tag.strip())
		if ver != '':
			uwscli.debug('version:', ver)
			v = semver.VersionInfo.parse(ver.split('-')[0])
			if v == t:
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

#
# main
#

__doc__ = 'auto build app latest release'

def main(argv = []):
	uwscli.debug('main')

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.autobuild_description())

	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	flags.add_argument('-d', '--deploy', action = 'store_true', default = False,
		help = 'app deploy')

	flags.add_argument('-n', '--dry-run', action = 'store_true', default = False,
		help = 'dry run')

	if '--deploy' in argv or '-d' in argv:
		flags.add_argument('app', metavar = 'app',
			help = 'app name')
		flags.add_argument('tag', metavar = 'tag',
			help = 'deploy app tag version')
	else:
		flags.add_argument('app', metavar = 'app',
			choices = uwscli.autobuild_list(), help = 'app name')

	args = flags.parse_args(argv)

	if not _setup():
		return ESETUP

	# autodeploy
	if args.deploy:
		app = args.app
		if app == 'crowdsourcing':
			app = 'cs'
		uwscli.debug('deploy:', app, 'tag', args.tag)
		return _deploy(app, args.tag)

	# autobuild
	return _build(args.app, dryrun = args.dry_run)
