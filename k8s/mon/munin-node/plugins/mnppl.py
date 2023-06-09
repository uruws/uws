#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from argparse import ArgumentParser
from pathlib  import Path

plugins_bindir = '/usr/local/bin'
plugins_suffix = '.mnppl'

def _listPlugins(bindir: str = '') -> list[str]:
	l = []
	for fn in os.listdir(bindir):
		fn = fn.strip()
		if fn.endswith(plugins_suffix):
			l.append(fn)
	return sorted(l)

__doc__ = 'munin-node parallel plugins runner'

def main(argv: list[str]):

	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-b', '--bindir', default = plugins_bindir, help = 'plugins bindir')

	args = flags.parse_args(argv)

	bindir = Path(args.bindir)

	for pl in _listPlugins(bindir):
		print(pl)

	return 0

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
