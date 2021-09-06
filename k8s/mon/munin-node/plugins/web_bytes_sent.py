# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	host = dict(),
)

def __parse(name, meta, value):
	global sts
	host = meta['host']
	if host == '_':
		host = 'default'
	mon.dbg('parse web_bytes_sent:', name, host)
	if not sts['host'].get(host, None):
		sts['host'][host] = dict(sum = 0, count = 0, meta = meta)
	sts['host'][host][name] += value
	return True

def parse(name, meta, value):
	if name == 'nginx_ingress_controller_bytes_sent_sum':
		return __parse('sum', meta, value)
	elif name == 'nginx_ingress_controller_bytes_sent_count':
		return __parse('count', meta, value)
	return False

def config(sts):
	mon.dbg('config web_bytes_sent')
	# host
	hn = 0
	for host in sorted(sts['host'].keys()):
		meta = sts['host'][host]['meta']
		hostid = mon.cleanfn(host)
		ingress = mon.cleanfn(meta['ingress'])
		# count
		print(f"multigraph web_bytes_sent_{hostid}_count")
		print(f"graph_title {host} bytes sent count")
		print('graph_args --base 1000 -l 0')
		print(f"graph_category {ingress}")
		print('graph_vlabel number')
		print('graph_scale yes')
		print('sent.label sent')
		print(f"sent.colour COLOUR{hn}")
		print('sent.min 0')
		# sum
		print(f"multigraph web_bytes_sent_{hostid}_sum")
		print(f"graph_title {host} bytes sent")
		print('graph_args --base 1024 -l 0')
		print(f"graph_category {ingress}")
		print('graph_vlabel bytes')
		print('graph_scale yes')
		print('sent.label sent')
		print(f"sent.colour COLOUR{hn}")
		print('sent.min 0')
		hn += 1

def report(sts):
	mon.dbg('report web_bytes_sent')
	for host in sorted(sts['host'].keys()):
		meta = sts['host'][host]['meta']
		hostid = mon.cleanfn(host)
		# count
		print(f"multigraph web_bytes_sent_{hostid}_count")
		print('sent.value', sts['host'][host]['count'])
		# sum
		print(f"multigraph web_bytes_sent_{hostid}_sum")
		print('sent.value', sts['host'][host]['sum'])
