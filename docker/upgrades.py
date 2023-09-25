#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import CalledProcessError
from subprocess import check_output

__doc__ = 'uws upgrades helper'

FROM_VERSION   = '2305'
TO_VERSION     = '2309'
REMOVE_VERSION = ['2211']

BUILD_SCRIPT = 'build.sh'

# utils

def git_ls(repo: str, pattern: str = '*') -> list[str]:
	out = check_output(f"/usr/bin/git -C {repo} ls-files {pattern}",
		timeout = 15, shell = True, text = True)
	return sorted(out.splitlines())

def git_grep(repo: str, pattern: str, args: str = '-Fl') -> list[str]:
	out = check_output(f"/usr/bin/git -C {repo} grep {args} '{pattern}'",
		timeout = 15, shell = True, text = True)
	return sorted(out.splitlines())

def date_version() -> str:
	return Path('./docker/VERSION').read_text().strip()

def replace(filename: str, src: str, dst: str):
	check_output(f"/usr/bin/sed -i 's#{src}#{dst}#g' {filename}",
		timeout = 15, shell = True, text = True)

def replace_docker_version(filename: str, version: str):
	check_output(f"/usr/bin/sed -i 's#^LABEL version=\".*#LABEL version=\"{version}\"#' {filename}", timeout = 15, shell = True, text = True)

def copyfn(src: str, dst: str):
	check_output(f"/usr/bin/cp -va {src} {dst}",
		timeout = 15, shell = True, text = True)

def build_script(repo: str, dstdir: str, tag: str, vfrom: str, vto: str):
	fn = Path(dstdir, BUILD_SCRIPT)
	srctag = '%s-%s' % (tag, vfrom)
	dsttag = '%s-%s' % (tag, vto)
	with fn.open('w') as fh:
		fh.write('#!/bin/sh\n')
		fh.write('set -eu\n')
		fh.write('# remove old versions\n')
		for vrm in REMOVE_VERSION:
			fh.write('docker rmi %s-%s || true\n' % (tag, vrm))
		fh.write('# %s\n' % srctag)
		fh.write('docker build --rm -t %s \\\n' % srctag)
		fh.write('\t-f %s/Dockerfile.%s \\\n' % (repo, vfrom))
		fh.write('\t./%s\n' % repo)
		fh.write('# %s\n' % dsttag)
		fh.write('docker build --rm -t %s \\\n' % dsttag)
		fh.write('\t-f %s/Dockerfile.%s \\\n' % (repo, vto))
		fh.write('\t./%s\n' % repo)
		fh.write('exit 0\n')
	print(fn)
	return 0

def writefile(name: str, data: str):
	fn = Path(name)
	with fn.open('w') as fh:
		fh.write(data)
	# ~ print(fn)

# commands

def fslist(repo):
	for fn in git_ls(repo, '*Dockerfile*'):
		print(Path(repo, fn))
	return 0

def upgrade_from_to(repo: str, tag: str, vfrom: str, vto: str):
	src = '%s-%s' % (tag, vfrom)
	dst = '%s-%s' % (tag, vto)
	for fpath in git_grep(repo, src):
		fn = Path(fpath).name.strip()
		if fn == BUILD_SCRIPT:
			continue
		elif fn.startswith('Dockerfile'):
			if fn.endswith('.devel'):
				pass
			elif fn.endswith('.%s' % vto):
				pass
			elif fn == 'Dockerfile':
				pass
			else:
				continue
		print(fpath)
		replace(fpath, src, dst)
		if fn == 'Dockerfile.devel':
			replace_docker_version(fpath, date_version())
	return 0

def check(repo, vfrom, vto):
	for fn in git_ls(repo, '*Dockerfile*.%s' % vfrom):
		dstfn = Path(repo, fn.replace(vfrom, vto, 1))
		if dstfn.exists():
			continue
		print(Path(repo, fn))
	return 0

def prune_docker(repo):
	for v in REMOVE_VERSION:
		for fn in git_ls(repo, '*Dockerfile*.%s' % v):
			p = Path(repo, fn)
			if p.exists() and p.is_file():
				print('remove:', p)
				p.unlink()
	return 0

def upgrade_docker(repo, vfrom, vto, tag, srctag):
	for fn in git_ls(repo, '*Dockerfile*.%s' % vfrom):
		srcfn = Path(repo, fn)
		dstfn = Path(repo, fn.replace(vfrom, vto, 1))
		if dstfn.exists():
			continue
		print(srcfn, '->', dstfn)
		copyfn(srcfn, dstfn)
		src = '%s-%s' % (srctag, vfrom)
		dst = '%s-%s' % (srctag, vto)
		replace(dstfn, src, dst)
		replace_docker_version(dstfn, date_version())
		dstdir = dstfn.parent
		build_script(repo, dstdir, tag, vfrom, vto)
	if repo == 'srv/munin':
		writefile('./k8s/mon/munin/VERSION', '%s\n' % date_version())
	elif repo == 'pod/base':
		writefile('./pod/test/VERSION', '%s\n' % date_version())
	elif repo == 'srv/munin':
		writefile('./k8s/mon/munin/VERSION', '%s\n' % date_version())
	return prune_docker(repo)

# main

def main(argv: list[str]) -> int:
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-F', '--from-version', metavar = FROM_VERSION, default = FROM_VERSION,
		help = 'upgrade from version')
	flags.add_argument('-T', '--to-version', metavar = TO_VERSION, default = TO_VERSION,
		help = 'upgrade to version')

	flags.add_argument('-t', '--tag', metavar = 'tag', default = '',
		help = 'docker tag')
	flags.add_argument('-s', '--source-tag', metavar = 'srctag', default = 'uws/base',
		help = 'docker source tag')

	flags.add_argument('-C', '--check', action = 'store_true', default = False,
		help = 'check upgrades')

	flags.add_argument('-U', '--upgrade', action = 'store_true', default = False,
		help = 'upgrade dockerfiles')

	flags.add_argument('repo', metavar = 'repo', default = '.',
		help = 'repo path', nargs = '?')

	args = flags.parse_args(argv)

	try:
		if args.check is True:
			return check(args.repo, args.from_version, args.to_version)
		elif args.upgrade is True:
			if args.tag == '':
				print('[ERROR] no tag', file = sys.stderr)
				return 1
			return upgrade_docker(args.repo, args.from_version, args.to_version, args.tag, args.source_tag)
		elif args.tag != '':
			return upgrade_from_to(args.repo, args.tag, args.from_version, args.to_version)
		else:
			fslist(args.repo)
	except CalledProcessError as err:
		print(err, file = sys.stderr)
		return err.returncode

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
