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
		m = dict(
			host = host,
		)
		sts['host'][host] = dict(sum = 0, count = 0, meta = m)
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
		# count
		print(f"multigraph web_sent_{hostid}")
		print(f"graph_title {host} sent")
		print('graph_args --base 1000 -l 0')
		print('graph_category web')
		print('graph_vlabel number')
		print('graph_scale yes')
		print('sent.label count')
		print(f"sent.colour COLOUR{hn}")
		print('sent.min 0')
		# count derive
		print(f"multigraph web_sent_{hostid}.count")
		print(f"graph_title {host} sent count")
		print('graph_args --base 1000 -l 0')
		print('graph_category web')
		print('graph_vlabel number per second')
		print('graph_scale yes')
		print('sent.label count')
		print(f"sent.colour COLOUR{hn}")
		print('sent.type DERIVE')
		print('sent.min 0')
		# sum
		print(f"multigraph web_sent_{hostid}_bytes")
		print(f"graph_title {host} bytes sent")
		print('graph_args --base 1024 -l 0')
		print('graph_category web')
		print('graph_vlabel bytes')
		print('graph_scale yes')
		print('sent.label sent')
		print(f"sent.colour COLOUR{hn}")
		print('sent.min 0')
		# sum derive
		print(f"multigraph web_sent_{hostid}_bytes.count")
		print(f"graph_title {host} bytes sent count")
		print('graph_args --base 1024 -l 0')
		print('graph_category web')
		print('graph_vlabel bytes per second')
		print('graph_scale yes')
		print('sent.label sent')
		print(f"sent.colour COLOUR{hn}")
		print('sent.type DERIVE')
		print('sent.min 0')
		hn += 1

def report(sts):
	mon.dbg('report web_bytes_sent')
	for host in sorted(sts['host'].keys()):
		meta = sts['host'][host]['meta']
		hostid = mon.cleanfn(host)
		# count
		print(f"multigraph web_sent_{hostid}")
		print('sent.value', sts['host'][host]['count'])
		print(f"multigraph web_sent_{hostid}.count")
		print('sent.value', sts['host'][host]['count'])
		# sum
		print(f"multigraph web_sent_{hostid}_bytes")
		print('sent.value', sts['host'][host]['sum'])
		print(f"multigraph web_sent_{hostid}_bytes.count")
		print('sent.value', sts['host'][host]['sum'])
