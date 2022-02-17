#!/usr/bin/env python3

import sys

from argparse   import ArgumentParser
from subprocess import CalledProcessError
from subprocess import check_output

__doc__ = "uws upgrades helper"

def git_ls(repo: str, pattern: str = '*') -> list[str]:
	out = check_output(f"/usr/bin/git -C {repo} ls-files {pattern}",
		timeout = 15, shell = True, text = True)
	return sorted(out.splitlines())

def main(argv: list[str]) -> int:
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('repo', metavar = 'repo', default = '.',
		help = 'repo path', nargs = '?')

	args = flags.parse_args(argv)

	try:
		for fn in git_ls(args.repo, '*Dockerfile*'):
			print(fn)
	except CalledProcessError as err:
		print(err, file = sys.stderr)
		return err.returncode

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
