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
	host = meta.get('host', '_')
	if host == '_':
		host = 'default'
	if not sts[ns][ingress].get(host, None):
		sts[ns][ingress][host] = dict()
	service = meta.get('service', '')
	if service == '':
		service = 'default'
	if not sts[ns][ingress][host].get(service, None):
		sts[ns][ingress][host][service] = dict(sum = 'U', count = 'U')
	mon.dbg('parse web_sent:', name, ns, ingress, host, service)
	if sts[ns][ingress][host][service][name] == 'U':
		sts[ns][ingress][host][service][name] = 0
	sts[ns][ingress][host][service][name] += value
	return True

SUM   = 'nginx_ingress_controller_bytes_sent_sum'
COUNT = 'nginx_ingress_controller_bytes_sent_count'

def parse(name, meta, value):
	if name == SUM:
		return __parse('sum', meta, value)
	elif name == COUNT:
		return __parse('count', meta, value)
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config web_sent')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# host
			hn = 0
			for host in sorted(sts[ns][ingress].keys()):
				# total
				hostid = mon.cleanfn(host)
				_print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}")
				_print(f"graph_title {ns}/{ingress} {host} sent total")
				_print('graph_args --base 1000 -l 0')
				_print('graph_category web_sent')
				_print('graph_vlabel number')
				_print('graph_scale yes')
				_print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					_print(f"{svcid}.label {svc}")
					_print(f"{svcid}.colour COLOUR{svcn}")
					_print(f"{svcid}.draw AREASTACK")
					_print(f"{svcid}.min 0")
					svcn = mon.color(svcn)
				if mon.debug(): _print()
				# count
				_print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}.count")
				_print(f"graph_title {ns}/{ingress} {host} sent")
				_print('graph_args --base 1000 -l 0')
				_print('graph_category web_sent')
				_print('graph_vlabel number per second')
				_print('graph_scale yes')
				_print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					_print(f"{svcid}.label {svc}")
					_print(f"{svcid}.colour COLOUR{svcn}")
					_print(f"{svcid}.draw AREASTACK")
					_print(f"{svcid}.type DERIVE")
					_print(f"{svcid}.min 0")
					_print(f"{svcid}.cdef {svcid},1000,/")
					svcn = mon.color(svcn)
				if mon.debug(): _print()
				# sum total
				_print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}")
				_print(f"graph_title {ns}/{ingress} {host} bytes sent total")
				_print('graph_args --base 1024 -l 0')
				_print('graph_category web_sent')
				_print('graph_vlabel bytes')
				_print('graph_scale yes')
				_print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					_print(f"{svcid}.label {svc}")
					_print(f"{svcid}.colour COLOUR{svcn}")
					_print(f"{svcid}.draw AREASTACK")
					_print(f"{svcid}.min 0")
					svcn = mon.color(svcn)
				if mon.debug(): _print()
				# sum count
				_print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}.count")
				_print(f"graph_title {ns}/{ingress} {host} bytes sent count")
				_print('graph_args --base 1024 -l 0')
				_print('graph_category web_sent')
				_print('graph_vlabel bytes per second')
				_print('graph_scale yes')
				_print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					_print(f"{svcid}.label {svc}")
					_print(f"{svcid}.colour COLOUR{svcn}")
					_print(f"{svcid}.draw AREASTACK")
					_print(f"{svcid}.type DERIVE")
					_print(f"{svcid}.min 0")
					_print(f"{svcid}.cdef {svcid},1000,/")
					svcn = mon.color(svcn)
				if mon.debug(): _print()

def report(sts):
	mon.dbg('report web_sent')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# host
			hn = 0
			for host in sorted(sts[ns][ingress].keys()):
				# total
				hostid = mon.cleanfn(host)
				# count
				_print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					_print(f"{svcid}.value", sts[ns][ingress][host][svc]['count'])
				if mon.debug(): _print()
				_print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}.count")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					value = mon.derive(sts[ns][ingress][host][svc]['count'])
					_print(f"{svcid}.value", value)
				if mon.debug(): _print()
				# sum
				_print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					_print(f"{svcid}.value", sts[ns][ingress][host][svc]['sum'])
				if mon.debug(): _print()
				_print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}.count")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					value = mon.derive(sts[ns][ingress][host][svc]['sum'])
					_print(f"{svcid}.value", value)
				if mon.debug(): _print()
