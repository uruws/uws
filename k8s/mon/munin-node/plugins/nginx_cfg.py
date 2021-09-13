# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon
import stats

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
	cfg = stats.Config()
	# hash
	h = stats.Graph('nginx_cfg_hash')
	h.title = 'Running config hash'
	h.category = 'nginx_cfg'
	h.vlabel = 'number'
	h.scale = True
	hf = stats.Field('hash')
	hf.label = 'hash'
	h.add(hf)
	cfg.add(h)
	# reload status
	r = stats.Graph('nginx_cfg_reload')
	r.title = 'Config reload status'
	r.upper = 1
	r.category = 'nginx_cfg'
	r.vlabel = 'successful reload'
	r.scale = True
	rf = stats.Field('reload')
	rf.label = 'reload'
	rf.draw = 'AREA'
	rf.max = 1
	r.add(rf)
	cfg.add(r)
	# reload uptime
	u = stats.Graph('nginx_cfg_uptime')
	u.title = 'Config uptime since last reload'
	u.category = 'nginx_cfg'
	u.vlabel = 'hours'
	uf = stats.Field('uptime')
	uf.draw = 'AREA'
	u.add(uf)
	cfg.add(u)
	# print
	cfg.print()

def report(sts):
	mon.dbg('report nginx_cfg')
	rpt = stats.Report()
	# hash
	h = stats.Graph('nginx_cfg_hash')
	hf = stats.Field('hash')
	hf.value = sts['config_hash']
	h.add(hf)
	rpt.add(h)
	# reload status
	r = stats.Graph('nginx_cfg_reload')
	rf = stats.Field('reload')
	rf.value = sts['config_last_reload_successful']
	r.add(rf)
	rpt.add(r)
	# reload uptime
	u = stats.Graph('nginx_cfg_uptime')
	uf = stats.Field('uptime')
	t = time() - sts['config_last_reload_successful_timestamp_seconds']
	uf.value = t / 3600.0
	u.add(uf)
	rpt.add(u)
	# print
	rpt.print()
