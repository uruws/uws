# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path

import semver

import uwscli

_appdata = Path('~/.uwscli/app-autobuild')

ESETUP = 10
ETAG   = 11

def _setup():
	try:
		uwscli.mkdir(_appdata)
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

	return 0
