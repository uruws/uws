# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from http         import HTTPStatus
from os           import getenv
from urllib.error import URLError

import mnpl_utils as utils

_category: str  = getenv('category', 'network').strip()
_app:      str  = getenv('app',      'app').strip()
_auth:     bool = getenv('auth',     'on').strip() == 'on'
_timeout:  str  = getenv('timeout',  '7').strip()
_target:   str  = getenv('target',   'http://localhost').strip()
_size_min: str  = getenv('size_min', '1500').strip()

_app_check:     str = getenv('app_check',     'meteor_runtime_config.js').strip()
_offline_check: str = getenv('offline_check', 'OFFLINEPAGEDEADBEEFCHECK').strip()

def config() -> int:
	utils.println('graph_title offline page', _target)
	utils.println('graph_args --base 1000 -l 0')
	utils.println('graph_category', _category)
	utils.println('graph_vlabel', _app)

	utils.println('a_running.label running')
	utils.println('a_running.colour COLOUR0')
	utils.println('a_running.draw AREASTACK')
	utils.println('a_running.min 0')
	utils.println('a_running.max 5')
	utils.println('a_running.critical 2:4')

	utils.println('b_offline.label offline')
	utils.println('b_offline.colour COLOUR1')
	utils.println('b_offline.draw AREASTACK')
	utils.println('b_offline.min 0')
	utils.println('b_offline.max 5')
	utils.println('b_offline.critical 2:4')

	utils.println('c_error.label error')
	utils.println('c_error.colour COLOUR2')
	utils.println('c_error.draw AREASTACK')
	utils.println('c_error.min 0')
	utils.println('c_error.max 5')
	utils.println('c_error.critical 2:4')

	utils.println('d_size.label size')
	utils.println('d_size.colour COLOUR3')
	utils.println('d_size.draw AREASTACK')
	utils.println('d_size.min 0')
	utils.println('d_size.max 5')
	utils.println('d_size.critical 2:4')
	return 0

def report() -> int:
	try:
		ttl = int(_timeout)
		size_min = int(_size_min)
	except ValueError as err:
		utils.error(err)
		ttl = 7
		size_min = 1500
	try:
		resp = utils.GET(_target, timeout = ttl, auth = _auth)
	except URLError as err:
		utils.error(err)
		utils.println('a_running.value U')
		utils.println('b_offline.value U')
		utils.println('c_error.value U')
		utils.println('d_size.value U')
		return 1
	error = '3.0'
	if resp.getcode() != HTTPStatus.OK:
		error = '1.0'
	offline_check = _offline_check.encode()
	app_check = _app_check.encode()
	running = '1.0'
	offline = '3.0'
	blen = 0
	with resp:
		for line in resp.readlines():
			blen += len(line) + 1
			# offline check
			if line.find(offline_check) >= 0:
				offline = '1.0'
			# app check
			if line.find(app_check) >= 0:
				running = '3.0'
	size = '3.0'
	if blen <= size_min:
		size = '1.0'
	utils.println('a_running.value', running)
	utils.println('b_offline.value', offline)
	utils.println('c_error.value', error)
	utils.println('d_size.value', size)
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
