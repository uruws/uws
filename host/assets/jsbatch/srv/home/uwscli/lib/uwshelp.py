# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser
from subprocess import check_output

import uwscli

def __out_split(out):
	lmax = 0
	lines = {}
	for l in out.splitlines():
		i = l.split(':', 1)
		lines[i[0]] = ':'.join(i[1:])
		llen = len(i[0])
		if llen > lmax:
			lmax = llen
	return (lmax, lines)

def all_help():
	cmd = "grep -sE '^__doc__' %s/*" % uwscli.bindir
	cmd += """ | sed "s/'//g" | sed "s#"""
	cmd += "%s\/" % uwscli.bindir
	cmd += '##" | sed "s/__doc__ = //"'
	out = check_output(cmd, shell = True, text = True)
	lmax, lines = __out_split(out)
	uwscli.log('uws command line interface')
	uwscli.log('')
	uwscli.log('available commands:')
	uwscli.log('')
	for c in lines.keys():
		uwscli.log('  ', c, ' '*(lmax - len(c)), ' - ', lines[c], sep = '')
	uwscli.log('')
	uwscli.log('run `uwshelp cmd` to get more information about cmd usage')
	return 0

def main(argv = []):
	flags = ArgumentParser(description = 'show uwscli commands help')
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('cmd', metavar = 'cmd', default = '', nargs = '?',
		help = 'command')

	args = flags.parse_args(argv)

	if args.cmd == '':
		return all_help()

	return uwscli.system("%s/%s --help" % (uwscli.bindir, args.cmd))
