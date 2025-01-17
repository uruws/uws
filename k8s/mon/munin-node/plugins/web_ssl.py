# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from time import gmtime, strftime, time

from typing import Any

import mon

sts: dict[str, Any] = dict()

def __parse(name: str, meta: dict[str, str], value: float) -> bool:
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

SUM = 'nginx_ingress_controller_ssl_expire_time_seconds'

def parse(name: str, meta: dict[str, str], value: float) -> bool:
	if name == SUM:
		return __parse('sum', meta, value)
	return False

def _print(*args):
	print(*args)

def config(sts: dict[str, Any]):
	mon.dbg('config web_ssl')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# host
		for host in sorted(sts[ns].keys()):
			hostid = mon.cleanfn(host)
			_print(f"multigraph web_ssl_{nsid}_{hostid}")
			_print(f"graph_title {host} ssl cert expire")
			_print('graph_args --base 1000')
			_print('graph_category web_ssl')
			_print('graph_vlabel days')
			_print('graph_scale no')
			_print('ssl.label expire')
			_print('ssl.colour COLOUR0')
			_print('ssl.draw AREA')
			value = sts[ns][host]
			_print('ssl.info', strftime('%c %z', gmtime(value)))
			_print('ssl.warning 20:')
			_print('ssl.critical 15:')
			if mon.debug(): _print()

def report(sts: dict[str, Any]):
	mon.dbg('report web_ssl')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# host
		for host in sorted(sts[ns].keys()):
			hostid = mon.cleanfn(host)
			_print(f"multigraph web_ssl_{nsid}_{hostid}")
			value = (sts[ns][host] - time()) / (24.0 * 3600.0)
			_print('ssl.value', value)
			if mon.debug(): _print()
