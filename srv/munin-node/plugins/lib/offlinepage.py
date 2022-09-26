# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from os import getenv

import mnpl_utils as utils

_category: str  = getenv('category', 'network').strip()
_app:      str  = getenv('app',      'app').strip()
_auth:     bool = getenv('auth',     'on').strip() == 'on'
_timeout:  str  = getenv('timeout',  '7').strip()
_target:   str  = getenv('target',   'http://localhost').strip()

def config() -> int:
	utils.println('graph_title offline page', _target)
	utils.println('graph_args --base 1000 -l 0')
	utils.println('graph_category', _category)
	utils.println('graph_vlabel', _app)
	utils.println('a_running.label running')
	utils.println('a_running.colour COLOUR0')
	utils.println('a_running.draw AREA')
	utils.println('a_running.min 0')
	utils.println('a_running.critical 1')
	utils.println('b_offline.label offline')
	utils.println('b_offline.colour COLOUR1')
	utils.println('b_offline.draw AREA')
	utils.println('b_offline.min 0')
	utils.println('b_offline.critical 1')
	utils.println('c_error.label error')
	utils.println('c_error.colour COLOUR2')
	utils.println('c_error.draw AREA')
	utils.println('c_error.min 0')
	utils.println('c_error.critical 1')
	return 0

def report() -> int:
	try:
		ttl = int(_timeout)
	except ValueError:
		ttl = 7
	resp = utils.GET(_target, timeout = ttl, auth = _auth)
	utils.println('a_running.value U')
	utils.println('b_offline.value U')
	utils.println('c_error.value U')
	return 0

def main(argv: list[str]) -> int:
	try:
		action = argv[0]
	except IndexError:
		action = 'report'
	if action == 'config':
		return config()
	return report()

if __name__ == '__main__': # pragma: no cover
	sys.exit(main(sys.argv[1:]))
