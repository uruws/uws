# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from time import sleep

import semver

import uwscli

_status_dir = '/run/uwscli/build'

ESETUP  = 10
ETAG    = 11
EBUILD  = 12
EDEPLOY = 13

def _setup():
	try:
		uwscli.mkdir(_status_dir)
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
	if tag > ver:
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
		return EBUILD
	sleep(1)
	rc = uwscli.nq("app-autobuild", f"{app} --deploy {tag}",
		bindir = "/srv/home/uwscli/bin")
	if rc != 0:
		return EDEPLOY
	return 0

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.build_description())
	flags.add_argument('app', metavar = 'app', choices = uwscli.build_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	if not _setup():
		return ESETUP

	build = uwscli.app[args.app].build
	with uwscli.chdir(build.dir):

		rc = uwscli.git_fetch(workdir = build.src)
		if rc != 0:
			return rc

		try:
			tag = _latestTag(build.src)
		except ValueError:
			uwscli.error('[ERROR] could not get latest git tag')
			return ETAG

		if _isBuildingOrDone(args.app, tag):
			return 0

		return _dispatch(args.app, tag)

	return 0
