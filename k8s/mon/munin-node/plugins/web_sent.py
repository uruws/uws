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

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_bytes_sent_sum':
		return __parse('sum', meta, value)
	elif name == 'nginx_ingress_controller_bytes_sent_count':
		return __parse('count', meta, value)
	return False

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
				print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}")
				print(f"graph_title {ns}/{ingress} {host} sent total")
				print('graph_args --base 1000 -l 0')
				print('graph_category web_sent')
				print('graph_vlabel number')
				print('graph_scale yes')
				print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					print(f"{svcid}.label {svc}")
					print(f"{svcid}.colour COLOUR{svcn}")
					print(f"{svcid}.draw AREASTACK")
					print(f"{svcid}.min 0")
					svcn += 1
				if mon.debug(): print()
				# count
				print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}.count")
				print(f"graph_title {ns}/{ingress} {host} sent")
				print('graph_args --base 1000 -l 0')
				print('graph_category web_sent')
				print('graph_vlabel number per second')
				print('graph_scale yes')
				print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					print(f"{svcid}.label {svc}")
					print(f"{svcid}.colour COLOUR{svcn}")
					print(f"{svcid}.draw AREASTACK")
					print(f"{svcid}.type DERIVE")
					print(f"{svcid}.min 0")
					print(f"{svcid}.cdef {svcid},1000,/")
					svcn += 1
				if mon.debug(): print()
				# sum total
				print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}")
				print(f"graph_title {ns}/{ingress} {host} bytes sent total")
				print('graph_args --base 1024 -l 0')
				print('graph_category web_sent')
				print('graph_vlabel bytes')
				print('graph_scale yes')
				print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					print(f"{svcid}.label {svc}")
					print(f"{svcid}.colour COLOUR{svcn}")
					print(f"{svcid}.draw AREASTACK")
					print(f"{svcid}.min 0")
					svcn += 1
				if mon.debug(): print()
				# sum count
				print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}.count")
				print(f"graph_title {ns}/{ingress} {host} bytes sent count")
				print('graph_args --base 1024 -l 0')
				print('graph_category web_sent')
				print('graph_vlabel bytes per second')
				print('graph_scale yes')
				print('graph_total total')
				svcn = 0
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					print(f"{svcid}.label {svc}")
					print(f"{svcid}.colour COLOUR{svcn}")
					print(f"{svcid}.draw AREASTACK")
					print(f"{svcid}.type DERIVE")
					print(f"{svcid}.min 0")
					print(f"{svcid}.cdef {svcid},1000,/")
					svcn += 1
				if mon.debug(): print()

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
				print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					print(f"{svcid}.value", sts[ns][ingress][host][svc]['count'])
				if mon.debug(): print()
				print(f"multigraph web_sent_{nsid}_{ingid}_{hostid}.count")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					value = mon.derive(sts[ns][ingress][host][svc]['count'])
					print(f"{svcid}.value", value)
				if mon.debug(): print()
				# sum
				print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					print(f"{svcid}.value", sts[ns][ingress][host][svc]['sum'])
				if mon.debug(): print()
				print(f"multigraph web_sent_bytes_{nsid}_{ingid}_{hostid}.count")
				for svc in sorted(sts[ns][ingress][host].keys()):
					svcid = mon.cleanfn(svc)
					value = mon.derive(sts[ns][ingress][host][svc]['sum'])
					print(f"{svcid}.value", value)
				if mon.debug(): print()
