#!/usr/bin/env python3

import sys

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import CalledProcessError
from subprocess import check_output

__doc__ = "uws upgrades helper"

FROM_VERSION = '2203'
TO_VERSION   = '2211'

# utils

def git_ls(repo: str, pattern: str = '*') -> list[str]:
	out = check_output(f"/usr/bin/git -C {repo} ls-files {pattern}",
		timeout = 15, shell = True, text = True)
	return sorted(out.splitlines())

def git_grep(repo: str, pattern: str, args: str = '-Fl') -> list[str]:
	out = check_output(f"/usr/bin/git -C {repo} grep {args} {pattern}",
		timeout = 15, shell = True, text = True)
	return sorted(out.splitlines())

def date_version() -> str:
	out = check_output(f"/usr/bin/date '+%y%m%d'",
		timeout = 15, shell = True, text = True)
	return out.splitlines()[0].strip()

def replace(filename: str, src: str, dst: str):
	check_output(f"/usr/bin/sed -i 's#{src}#{dst}#g' {filename}",
		timeout = 15, shell = True, text = True)

def replace_docker_version(filename: str, version: str):
	check_output(f"/usr/bin/sed -i 's#^LABEL version=\".*#LABEL version=\"{version}\"#' {filename}", timeout = 15, shell = True, text = True)

def copyfn(src: str, dst: str):
	check_output(f"/usr/bin/cp -va {src} {dst}",
		timeout = 15, shell = True, text = True)

# commands

def fslist(repo):
	for fn in git_ls(repo, '*Dockerfile*'):
		print(Path(repo, fn))

def upgrade_from_to(repo: str, tag: str, vfrom: str, vto: str):
	src = '%s-%s' % (tag, vfrom)
	dst = '%s-%s' % (tag, vto)
	for fn in git_grep(repo, src):
		if fn.endswith('build.sh'):
			continue
		print(fn)
		replace(fn, src, dst)
	return 0

def check(repo, vfrom, vto):
	for fn in git_ls(repo, '*Dockerfile.%s' % vfrom):
		dstfn = Path(repo, fn.replace(vfrom, vto, 1))
		if dstfn.exists():
			continue
		print(Path(repo, fn))

def upgrade_docker(repo, vfrom, vto, tag):
	for fn in git_ls(repo, '*Dockerfile.%s' % vfrom):
		srcfn = Path(repo, fn)
		dstfn = Path(repo, fn.replace(vfrom, vto, 1))
		if dstfn.exists():
			continue
		print(srcfn)
		copyfn(srcfn, dstfn)
		srctag = '%s-%s' % (tag, vfrom)
		dsttag = '%s-%s' % (tag, vto)
		replace(dstfn, srctag, dsttag)
		replace_docker_version(dstfn, date_version())

# main

def main(argv: list[str]) -> int:
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-F', '--from-version', metavar = FROM_VERSION, default = FROM_VERSION,
		help = 'upgrade from version')
	flags.add_argument('-T', '--to-version', metavar = TO_VERSION, default = TO_VERSION,
		help = 'upgrade to version')

	flags.add_argument('-t', '--tag', metavar = 'tag', default = '',
		help = 'docker tag')

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
			return upgrade_docker(args.repo, args.from_version, args.to_version, args.tag)
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
