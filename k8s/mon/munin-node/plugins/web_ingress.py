# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Any

import mon

sts: dict[str, Any] = dict()

def __parse(meta: dict[str, str], value: float) -> bool:
	global sts
	ns = meta.get('namespace', '')
	if ns == '':
		ns = 'default'
	if not sts.get(ns, None):
		sts[ns] = dict()
	ingress = meta.get('ingress', '')
	if ingress == '':
		ingress = 'default'
	if not sts[ns].get(ingress, None):
		sts[ns][ingress] = dict()
	service = meta.get('service', '')
	if service == '':
		service = 'default'
	if not sts[ns][ingress].get(service, None):
		sts[ns][ingress][service] = dict()
	status = meta.get('status', '')
	if status == '':
		status = 'unknown'
	if not sts[ns][ingress][service].get(status, None):
		sts[ns][ingress][service][status] = 0
	mon.dbg('parse web_ingress:', ns, ingress, service, status)
	sts[ns][ingress][service][status] += value
	return True

REQUESTS = 'nginx_ingress_controller_requests'

def parse(name: str, meta: dict[str, str], value: float) -> bool:
	if name == REQUESTS:
		return __parse(meta, value)
	return False

def _print(*args):
	print(*args)

def config(sts: dict[str, Any]):
	mon.dbg('config web_ingress')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# service
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				# total
				_print(f"multigraph web_ingress_{nsid}_{ingid}_{svcid}")
				_print(f"graph_title {ns}/{ingress} {svc} client requests total")
				_print('graph_args --base 1000 -l 0')
				_print('graph_category web_ingress')
				_print('graph_vlabel number')
				_print('graph_scale yes')
				_print('graph_total total')
				stn = 0
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					_print(f"status_{stid}.label {st}")
					_print(f"status_{stid}.colour COLOUR{stn}")
					_print(f"status_{stid}.draw AREASTACK")
					_print(f"status_{stid}.min 0")
					stn = mon.color(stn)
				if mon.debug(): _print()
				# count
				_print(f"multigraph web_ingress_{nsid}_{ingid}_{svcid}.count")
				_print(f"graph_title {ns}/{ingress} {svcid} client requests")
				_print('graph_args --base 1000 -l 0')
				_print('graph_category web_ingress')
				_print('graph_vlabel number per second')
				_print('graph_scale yes')
				_print('graph_total total')
				stn = 0
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					_print(f"status_{stid}.label {st}")
					_print(f"status_{stid}.colour COLOUR{stn}")
					_print(f"status_{stid}.draw AREASTACK")
					_print(f"status_{stid}.type DERIVE")
					_print(f"status_{stid}.min 0")
					_print(f"status_{stid}.cdef status_{stid},1000,/")
					stn = mon.color(stn)
				if mon.debug(): _print()

def report(sts: dict[str, Any]):
	mon.dbg('report web_ingress')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# service
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				# total
				_print(f"multigraph web_ingress_{nsid}_{ingid}_{svcid}")
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					value = sts[ns][ingress][svc][st]
					_print(f"status_{stid}.value {value}")
				if mon.debug(): _print()
				# count
				_print(f"multigraph web_ingress_{nsid}_{ingid}_{svcid}.count")
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					value = mon.derive(sts[ns][ingress][svc][st])
					_print(f"status_{stid}.value {value}")
				if mon.debug(): _print()
