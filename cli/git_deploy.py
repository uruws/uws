#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser
from os import path

sys.path.insert(0, '/srv/home/uwscli/lib')
import uwscli
import uwscli_conf

__doc__ = 'uws git deploy'

def _getTag(tagref):
	return '/'.join(tagref.split('/')[2:])

def _getRepo(rpath):
	return rpath.split('/')[-1].replace('.git', '')

def _getTestDir(rname):
	return '/'.join([uwscli_conf.deploy_testdir, rname])

def main(argv = []):
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-r', '--repo', metavar = 'PATH', required = True,
		help = 'origin repo path')
	flags.add_argument('-t', '--tagref', metavar = 'git/tag/ref', required = True,
		help = 'pushed tag refname')

	args = flags.parse_args(argv)

	if not args.tagref.startswith('refs/tags/'):
		uwscli.error('[ERROR] not a tag reference:', args.tagref)
		return 1

	if not args.repo.endswith('.git'):
		uwscli.error('[ERROR] invalid repo path:', args.repo)
		return 2

	tag = _getTag(args.tagref)
	rname = _getRepo(args.repo)
	rtest = _getTestDir(rname)

	if not path.exists(rtest):
		with uwscli.chdir(uwscli_conf.deploy_testdir, error_status = 3):
			if uwscli.git_clone(args.repo) != 0:
				return 4

	with uwscli.chdir(rtest, error_status = 5):
		pass

	return 0

if __name__ == '__main__': # pragma: no coverage
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
