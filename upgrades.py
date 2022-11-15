#!/usr/bin/env python3

import sys

from argparse   import ArgumentParser
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

def replace(filename: str, src: str, dst: str):
	check_output(f"/usr/bin/sed -i 's#{src}#{dst}#g' {filename}",
		timeout = 15, shell = True, text = True)

# commands

def fslist(args):
	for fn in git_ls(args.repo, '*Dockerfile*'):
		print('%s/%s' % (args.repo, fn))

def upgrade_from_to(repo: str, tag: str, vfrom: str, vto: str):
	src = '%s-%s' % (tag, vfrom)
	dst = '%s-%s' % (tag, vto)
	for fn in git_grep(repo, src):
		if fn.endswith('build.sh'):
			continue
		print(fn)
		replace(fn, src, dst)
	return 0

# main

def main(argv: list[str]) -> int:
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-F', '--from-version', metavar = FROM_VERSION, default = FROM_VERSION,
		help = 'upgrade from version')
	flags.add_argument('-T', '--to-version', metavar = TO_VERSION, default = TO_VERSION,
		help = 'upgrade to version')

	flags.add_argument('-t', '--tag', metavar = 'tag', default = '',
		help = 'docker tag')

	flags.add_argument('repo', metavar = 'repo', default = '.',
		help = 'repo path', nargs = '?')

	args = flags.parse_args(argv)

	try:
		if args.from_version != '':
			if args.to_version == '':
				print('no --to-version', file = sys.stderr)
				return 1
			if args.tag == '':
				print('no --tag', file = sys.stderr)
				return 2
			return upgrade_from_to(args.repo, args.tag, args.from_version, args.to_version)
		else:
			fslist(args)
	except CalledProcessError as err:
		print(err, file = sys.stderr)
		return err.returncode

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
