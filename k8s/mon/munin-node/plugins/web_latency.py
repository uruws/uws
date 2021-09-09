# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

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

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_ingress_upstream_latency_seconds_sum':
		return __parse('sum', meta, value)
	elif name == 'nginx_ingress_controller_ingress_upstream_latency_seconds_count':
		return True
		# ~ return __parse('count', meta, value)
	return False

def config(sts):
	mon.dbg('config web_latency')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# sum
			print(f"multigraph web_latency_{nsid}_{ingid}")
			print(f"graph_title {ns}/{ingress} service latency total")
			print('graph_args --base 1000 -l 0')
			print('graph_category web')
			print('graph_vlabel seconds')
			print('graph_scale no')
			print('graph_total total')
			svcn = 0
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				print(f"{svcid}.label {svc}")
				print(f"{svcid}.colour COLOUR{svcn}")
				print(f"{svcid}.draw AREASTACK")
				print(f"{svcid}.min 0")
				svcn += 1
			if mon.debug(): print()
			# sum derive
			print(f"multigraph web_latency_{nsid}_{ingid}.count")
			print(f"graph_title {ns}/{ingress} service latency")
			print('graph_args --base 1000 -l 0')
			print('graph_category web')
			print('graph_vlabel latency per second')
			print('graph_scale no')
			print('graph_total total')
			svcn = 0
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				print(f"{svcid}.label {svc} seconds")
				print(f"{svcid}.colour COLOUR{svcn}")
				print(f"{svcid}.draw AREASTACK")
				print(f"{svcid}.type DERIVE")
				print(f"{svcid}.min 0")
				svcn += 1
			if mon.debug(): print()

def report(sts):
	mon.dbg('report web_latency')
	# ns
	for ns in sorted(sts.keys()):
		nsid = mon.cleanfn(ns)
		# ingress
		for ingress in sorted(sts[ns].keys()):
			ingid = mon.cleanfn(ingress)
			# sum
			print(f"multigraph web_latency_{nsid}_{ingid}")
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				value = sts[ns][ingress][svc]['sum']
				print(f"{svcid}.value {value}")
			if mon.debug(): print()
			# sum derive
			print(f"multigraph web_latency_{nsid}_{ingid}.count")
			for svc in sorted(sts[ns][ingress].keys()):
				svcid = mon.cleanfn(svc)
				value = sts[ns][ingress][svc]['sum']
				print(f"{svcid}.value {value}")
			if mon.debug(): print()
