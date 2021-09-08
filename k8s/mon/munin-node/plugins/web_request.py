# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict()

def __parse(meta, value):
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
	mon.dbg('parse web_request:', ns, ingress, service, status)
	sts[ns][ingress][service][status] += value
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_requests':
		return __parse(meta, value)
	return False

def config(sts):
	mon.dbg('config web_request')
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
				print(f"multigraph {nsid}_{ingid}_{svcid}_web_request")
				print(f"graph_title {ns}/{ingress} {svc} client requests total")
				print('graph_args --base 1000 -l 0')
				print('graph_category web')
				print('graph_vlabel number')
				print('graph_scale yes')
				print('graph_total total')
				stn = 0
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					print(f"status_{stid}.label {st}")
					print(f"status_{stid}.colour COLOUR{stn}")
					print(f"status_{stid}.draw AREASTACK")
					print(f"status_{stid}.min 0")
					stn += 1
				if mon.debug(): print()
				# count
				print(f"multigraph {nsid}_{ingid}_{svcid}_web_request.count")
				print(f"graph_title {ns}/{ingress} {svcid} client requests")
				print('graph_args --base 1000 -l 0')
				print('graph_category web')
				print('graph_vlabel number per second')
				print('graph_scale yes')
				print('graph_total total')
				stn = 0
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					print(f"status_{stid}.label {st}")
					print(f"status_{stid}.colour COLOUR{stn}")
					print(f"status_{stid}.draw AREASTACK")
					print(f"status_{stid}.type DERIVE")
					print(f"status_{stid}.min 0")
					stn += 1
				if mon.debug(): print()

def report(sts):
	mon.dbg('report web_request')
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
				print(f"multigraph {nsid}_{ingid}_{svcid}_web_request")
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					value = sts[ns][ingress][svc][st]
					print(f"status_{stid}.value {value}")
				if mon.debug(): print()
				# count
				print(f"multigraph {nsid}_{ingid}_{svcid}_web_request.count")
				for st in sorted(sts[ns][ingress][svc].keys()):
					stid = mon.cleanfn(st)
					value = sts[ns][ingress][svc][st]
					print(f"status_{stid}.value {value}")
				if mon.debug(): print()
