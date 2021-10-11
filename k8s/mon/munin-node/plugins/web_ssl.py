# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from time import gmtime, strftime, time

import mon

sts = dict()

def __parse(name, meta, value):
	global sts
	ns = meta.get('namespace', '')
	if ns == '':
		ns = 'default'
	if not sts.get(ns, None):
		sts[ns] = dict()
	host = meta.get('host', '_')
	if host == '_':
		host = 'default'
	mon.dbg('parse web_ssl:', ns, host)
	sts[ns][host] = value
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_ssl_expire_time_seconds':
		return __parse('sum', meta, value)
	return False

def config(sts):
	mon.dbg('config web_ssl')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# host
		for host in sorted(sts[ns].keys()):
			hostid = mon.cleanfn(host)
			print(f"multigraph web_ssl_{nsid}_{hostid}")
			print(f"graph_title {host} ssl cert expire")
			print('graph_args --base 1000')
			print('graph_category web_ssl')
			print('graph_vlabel days')
			print('graph_scale no')
			print('ssl.label expire')
			print('ssl.colour COLOUR0')
			print('ssl.draw AREA')
			value = sts[ns][host]
			print('ssl.info', strftime('%c %z', gmtime(value)))
			print('ssl.warning 20:')
			print('ssl.critical 15:')
			if mon.debug(): print()

def report(sts):
	mon.dbg('report web_ssl')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# host
		for host in sorted(sts[ns].keys()):
			hostid = mon.cleanfn(host)
			print(f"multigraph web_ssl_{nsid}_{hostid}")
			value = (sts[ns][host] - time()) / (24.0 * 3600.0)
			print('ssl.value', value)
			if mon.debug(): print()
