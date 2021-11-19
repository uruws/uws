#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse import ArgumentParser
from os import environ, path

sys.path.insert(0, '/srv/home/uwscli/lib')
import uwscli
import uwscli_conf

__doc__ = 'uws git deploy'

ETAGREF         = 1
ERPATH          = 2
ETESTDIR        = 3
ETESTCLONE      = 4
ERTEST_DIR      = 5
ERTEST_FETCH    = 6
ERTEST_CHECKOUT = 7
EDEPLOY         = 8

# ~ EBASEDIR = 5
# ~ ECLONE = 6

def _getTag(tagref):
	return '/'.join(tagref.split('/')[2:])

def _getRepo(rpath):
	return rpath.split('/')[-1].replace('.git', '')

def _getTestDir(rname):
	return '/'.join([uwscli_conf.deploy_testdir, rname])

# ~ def _getDeployDir(rname):
	# ~ return '/'.join([uwscli_conf.deploy_basedir, rname])

def main(argv = []):
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-r', '--repo', metavar = 'PATH', required = True,
		help = 'origin repo path')
	flags.add_argument('-t', '--tagref', metavar = 'git/tag/ref', required = True,
		help = 'pushed tag refname')

	args = flags.parse_args(argv)

	if not args.tagref.startswith('refs/tags/'):
		uwscli.error('[ERROR] not a tag reference:', args.tagref)
		return ETAGREF

	if not args.repo.endswith('.git'):
		uwscli.error('[ERROR] invalid repo path:', args.repo)
		return ERPATH

	tag = _getTag(args.tagref)
	rname = _getRepo(args.repo)
	rtest = _getTestDir(rname)

	environ['GIT_DIR'] = '.'

	if not path.exists(rtest):
		with uwscli.chdir(uwscli_conf.deploy_testdir, error_status = ETESTDIR):
			if uwscli.git_clone(args.repo) != 0:
				return ETESTCLONE

	with uwscli.chdir(rtest, error_status = ERTEST_DIR):
		if uwscli.git_fetch() != 0:
			return ERTEST_FETCH
		if uwscli.git_checkout(tag) != 0:
			return ERTEST_CHECKOUT
		if uwscli.git_deploy(rname, tag) != 0:
			return EDEPLOY

	# ~ rdeploy = _getDeployDir(rname)
	# ~ if not path.exists(rdeploy):
		# ~ with uwscli.chdir(uwscli_conf.deploy_basedir, error_status = EBASEDIR):
			# ~ if uwscli.git_clone(args.repo) != 0:
				# ~ return ECLONE

	return 0

if __name__ == '__main__': # pragma: no coverage
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
