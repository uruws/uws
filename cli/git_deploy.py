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

ETAGREF        = 1
EREPO          = 2
EDIR           = 3
ECLONE         = 4
EREPO_DIR      = 5
EREPO_FETCH    = 6
EREPO_CHECKOUT = 7
EDEPLOY        = 8

def _getTag(tagref):
	return '/'.join(tagref.split('/')[2:])

def _getRepo(rpath):
	return rpath.split('/')[-1].replace('.git', '')

def _getDeployDir(rname):
	return '/'.join([uwscli_conf.deploy_basedir, rname])

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
		uwscli.error('[ERROR] invalid repo:', args.repo)
		return EREPO

	tag = _getTag(args.tagref)
	rname = _getRepo(args.repo)
	rdir = _getDeployDir(rname)

	environ['GIT_DIR'] = '.'

	if not path.exists(rdir):
		with uwscli.chdir(uwscli_conf.deploy_basedir, error_status = EDIR):
			if uwscli.git_clone(args.repo) != 0:
				return ECLONE

	with uwscli.chdir(rdir, error_status = EREPO_DIR):
		if uwscli.git_fetch() != 0:
			return EREPO_FETCH
		if uwscli.git_checkout(tag) != 0:
			return EREPO_CHECKOUT
		if uwscli.git_deploy(rname, tag) != 0:
			return EDEPLOY

	return 0

if __name__ == '__main__': # pragma: no coverage
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
