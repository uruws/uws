# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	config_hash = 'U',
	config_last_reload_successful = 'U',
	config_last_reload_successful_timestamp_seconds = 'U',
)

def __parse(name, value):
	mon.dbg('parse nginx_cfg:', name)
	sts[name] = value
	return True

def parse(name, meta, value):
	if name.startswith('nginx_ingress_controller_config_'):
		name = name.replace('nginx_ingress_controller_config_', 'config_', 1)
		return __parse(name, value)
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config nginx_cfg')
	# hash
	_print('multigraph nginx_cfg_hash')
	_print('graph_title Running config hash')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_cfg')
	_print('graph_vlabel number')
	_print('graph_scale yes')
	_print('hash.label hash')
	_print('hash.colour COLOUR0')
	_print('hash.min 0')
	# reload status
	_print('multigraph nginx_cfg_reload')
	_print('graph_title Config reload status')
	_print('graph_args --base 1000 -l 0 -u 1')
	_print('graph_category nginx_cfg')
	_print('graph_vlabel successful reload')
	_print('graph_scale yes')
	_print('reload.label reload')
	_print('reload.colour COLOUR0')
	_print('reload.draw AREA')
	_print('reload.min 0')
	_print('reload.max 1')
	# reload uptime
	_print('multigraph nginx_cfg_uptime')
	_print('graph_title Config uptime since last reload')
	_print('graph_args --base 1000 -l 0')
	_print('graph_category nginx_cfg')
	_print('graph_vlabel hours')
	_print('graph_scale no')
	_print('uptime.label uptime')
	_print('uptime.colour COLOUR0')
	_print('uptime.draw AREA')
	_print('uptime.min 0')

def report(sts):
	mon.dbg('report nginx_cfg')
	# hash
	_print('multigraph nginx_cfg_hash')
	_print('hash.value', sts['config_hash'])
	# reload status
	_print('multigraph nginx_cfg_reload')
	_print('reload.value', sts['config_last_reload_successful'])
	# reload uptime
	_print('multigraph nginx_cfg_uptime')
	t = time() - sts['config_last_reload_successful_timestamp_seconds']
	_print('uptime.value', t / 3600.0)
