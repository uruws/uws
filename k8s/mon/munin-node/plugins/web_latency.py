# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict()

def __parse(name, meta, value):
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
	mon.dbg('parse web_latency:', name, ns, ingress, service)
	sts[ns][ingress][service][name] = value
	return True

SUM   = 'nginx_ingress_controller_ingress_upstream_latency_seconds_sum'
COUNT = 'nginx_ingress_controller_ingress_upstream_latency_seconds_count'

def parse(name, meta, value):
	if name == SUM:
		return __parse('sum', meta, value)
	elif name == COUNT:
		return True
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config web_latency')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# sum
			_print(f"multigraph web_latency_{nsid}_{ingid}")
			_print(f"graph_title {ns}/{ingress} service latency total")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category web_latency')
			_print('graph_vlabel seconds')
			_print('graph_scale no')
			_print('graph_total total')
			svcn = 0
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				_print(f"{svcid}.label {svc}")
				_print(f"{svcid}.colour COLOUR{svcn}")
				_print(f"{svcid}.draw AREASTACK")
				_print(f"{svcid}.min 0")
				svcn = mon.color(svcn)
			if mon.debug(): _print()
			# sum derive
			_print(f"multigraph web_latency_{nsid}_{ingid}.count")
			_print(f"graph_title {ns}/{ingress} service latency")
			_print('graph_args --base 1000 -l 0')
			_print('graph_category web_latency')
			_print('graph_vlabel latency per second')
			_print('graph_scale no')
			_print('graph_total total')
			svcn = 0
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				_print(f"{svcid}.label {svc} seconds")
				_print(f"{svcid}.colour COLOUR{svcn}")
				_print(f"{svcid}.draw AREASTACK")
				_print(f"{svcid}.type DERIVE")
				_print(f"{svcid}.min 0")
				_print(f"{svcid}.cdef {svcid},1000,/")
				svcn = mon.color(svcn)
			if mon.debug(): _print()

def report(sts):
	mon.dbg('report web_latency')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# sum
			_print(f"multigraph web_latency_{nsid}_{ingid}")
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				value = sts[ns][ingress][svc].get('sum', 'U')
				_print(f"{svcid}.value {value}")
			if mon.debug(): _print()
			# sum derive
			_print(f"multigraph web_latency_{nsid}_{ingid}.count")
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				value = mon.derive(sts[ns][ingress][svc].get('sum', 'U'))
				_print(f"{svcid}.value {value}")
			if mon.debug(): _print()
