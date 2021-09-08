# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	ingress = dict(),
)

def __parse(name, meta, value):
	global sts
	ingress = meta['ingress']
	if ingress == '':
		ingress = 'default'
	service = meta['service']
	if service == '':
		service = 'default'
	mon.dbg('parse web_latency:', name, ingress, service)
	if not sts['ingress'].get(ingress, None):
		sts['ingress'][ingress] = dict()
	if not sts['ingress'][ingress].get(service, None):
		sts['ingress'][ingress][service] = dict(count = 'U', sum = 'U')
	sts['ingress'][ingress][service][name] = value
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
	# ingress
	for ingress in sorted(sts['ingress'].keys()):
		ingid = mon.cleanfn(ingress)
		# sum
		print(f"multigraph web_latency_{ingid}")
		print(f"graph_title {ingress} service latency")
		print('graph_args --base 1000 -l 0')
		print('graph_category web')
		print('graph_vlabel seconds')
		print('graph_scale no')
		svcn = 0
		for svc in sorted(sts['ingress'][ingress].keys()):
			svcid = mon.cleanfn(svc)
			print(f"{svcid}.label {svc}")
			print(f"{svcid}.colour COLOUR{svcn}")
			print(f"{svcid}.min 0")
			svcn += 1
		# sum derive
		print(f"multigraph web_latency_{ingid}.count")
		print(f"graph_title {ingress} service latency count")
		print('graph_args --base 1000 -l 0')
		print('graph_category web')
		print('graph_vlabel latency per second')
		print('graph_scale no')
		svcn = 0
		for svc in sorted(sts['ingress'][ingress].keys()):
			svcid = mon.cleanfn(svc)
			print(f"{svcid}.label {svc} seconds")
			print(f"{svcid}.colour COLOUR{svcn}")
			print(f"{svcid}.type DERIVE")
			print(f"{svcid}.min 0")
			svcn += 1

def report(sts):
	mon.dbg('report web_latency')
	# ingress
	for ingress in sorted(sts['ingress'].keys()):
		ingid = mon.cleanfn(ingress)
		# sum
		print(f"multigraph web_latency_{ingid}")
		for svc in sorted(sts['ingress'][ingress].keys()):
			svcid = mon.cleanfn(svc)
			value = sts['ingress'][ingress][svc]['sum']
			print(f"{svcid}.value {value}")
		# sum derive
		print(f"multigraph web_latency_{ingid}.count")
		for svc in sorted(sts['ingress'][ingress].keys()):
			svcid = mon.cleanfn(svc)
			value = sts['ingress'][ingress][svc]['sum']
			print(f"{svcid}.value {value}")
