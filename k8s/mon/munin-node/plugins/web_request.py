# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict()

def __parse(meta, value):
	global sts
	ingress = meta['ingress']
	if ingress == '':
		ingress = 'default'
	service = meta['service']
	if service == '':
		service = 'default'
	status = meta['status']
	if status == '':
		status = 'unknown'
	mon.dbg('parse web_request:', ingress, service, status)
	if not sts.get(ingress, None):
		sts[ingress] = dict()
	if not sts[ingress].get(service, None):
		sts[ingress][service] = dict()
	if not sts[ingress][service].get(status, None):
		sts[ingress][service][status] = 0
	sts[ingress][service][status] += value
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_requests':
		return __parse(meta, value)
	return False

def config(sts):
	mon.dbg('config web_request')
	# ingress
	for ingress in sorted(sts.keys()):
		ingid = mon.cleanfn(ingress)
		# service
		for svc in sorted(sts[ingress].keys()):
			svcid = mon.cleanfn(svc)
			# total
			print(f"multigraph {ingid}_{svcid}_web_request")
			print(f"graph_title {ingress} {svcid} client requests")
			print('graph_args --base 1000 -l 0')
			print('graph_category web')
			print('graph_vlabel number')
			print('graph_scale yes')
			print('graph_total total')
			stn = 0
			for st in sorted(sts[ingress][svc].keys()):
				stid = mon.cleanfn(st)
				print(f"status_{stid}.label {st}")
				print(f"status_{stid}.colour COLOUR{stn}")
				print(f"status_{stid}.draw AREASTACK")
				print(f"status_{stid}.min 0")
				stn += 1
			# count
			print(f"multigraph {ingid}_{svcid}_web_request.count")
			print(f"graph_title {ingress} {svcid} client requests count")
			print('graph_args --base 1000 -l 0')
			print('graph_category web')
			print('graph_vlabel number per second')
			print('graph_scale yes')
			print('graph_total total')
			stn = 0
			for st in sorted(sts[ingress][svc].keys()):
				stid = mon.cleanfn(st)
				print(f"status_{stid}.label {st}")
				print(f"status_{stid}.colour COLOUR{stn}")
				print(f"status_{stid}.draw AREASTACK")
				print(f"status_{stid}.type DERIVE")
				print(f"status_{stid}.min 0")
				stn += 1

def report(sts):
	mon.dbg('report web_request')
	# ingress
	for ingress in sorted(sts.keys()):
		ingid = mon.cleanfn(ingress)
		# service
		for svc in sorted(sts[ingress].keys()):
			svcid = mon.cleanfn(svc)
			# total
			print(f"multigraph {ingid}_{svcid}_web_request")
			for st in sorted(sts[ingress][svc].keys()):
				stid = mon.cleanfn(st)
				value = sts[ingress][svc][st]
				print(f"status_{stid}.value {value}")
			# count
			print(f"multigraph {ingid}_{svcid}_web_request.count")
			for st in sorted(sts[ingress][svc].keys()):
				stid = mon.cleanfn(st)
				value = sts[ingress][svc][st]
				print(f"status_{stid}.value {value}")
