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

def config(sts):
	mon.dbg('config nginx_cfg')
	# hash
	print('multigraph nginx_cfg_hash')
	print('graph_title Running config hash')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number')
	print('graph_scale yes')
	print('hash.label hash')
	print('hash.colour COLOUR0')
	print('hash.min 0')
	# reload status
	print('multigraph nginx_cfg_reload')
	print('graph_title Config reload status')
	print('graph_args --base 1000 -l 0 -u 1')
	print('graph_category nginx')
	print('graph_vlabel successful reload')
	print('graph_scale yes')
	print('reload.label reload')
	print('reload.colour COLOUR0')
	print('reload.draw AREA')
	print('reload.min 0')
	print('reload.max 1')
	# reload uptime
	print('multigraph nginx_cfg_uptime')
	print('graph_title Config uptime since last reload')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel hours')
	print('graph_scale no')
	print('uptime.label uptime')
	print('uptime.colour COLOUR0')
	print('uptime.draw AREA')
	print('uptime.min 0')

def report(sts):
	mon.dbg('report nginx_cfg')
	# hash
	print('multigraph nginx_cfg_hash')
	print('hash.value', sts['config_hash'])
	# reload status
	print('multigraph nginx_cfg_reload')
	print('reload.value', sts['config_last_reload_successful'])
	# reload uptime
	print('multigraph nginx_cfg_uptime')
	t = time() - sts['config_last_reload_successful_timestamp_seconds']
	print('uptime.value', t / 3600.0)
