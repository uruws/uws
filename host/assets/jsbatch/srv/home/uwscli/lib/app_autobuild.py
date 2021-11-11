# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import chdir, system
from subprocess import getstatusoutput

import uwscli

def lastTag(app):
	src = uwscli.app[app].build.src
	ref = uwscli.app[app].build.ref
	return getstatusoutput(f"git -C {src} describe --abbrev=0 --tags {ref}")

def main(argv = []):
	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = uwscli.build_description())
	flags.add_argument('app', metavar = 'app', choices = uwscli.build_list(),
		default = 'app', help = 'app name')

	args = flags.parse_args(argv)

	bdir = uwscli.app[args.app].build.dir
	chdir(bdir)

	rc, tag = lastTag(args.app)
	if rc != 0:
		uwscli.error(tag)
		return rc
	uwscli.log('Build tag:', tag)

	return 0
