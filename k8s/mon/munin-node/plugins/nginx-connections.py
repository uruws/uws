#!/usr/bin/env python3

import math
import os
import sys

from urllib.request import urlopen

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)
import mon

def parse(resp):
	mon.dbg('parse')
	sts = dict(
		active = 'U',
		reading = 'U',
		waiting = 'U',
		writing = 'U',
		accepted = 'U',
		handled = 'U',
	)
	for line in resp.read().decode().splitlines():
		if line.startswith('#'):
			continue
		elif line == '':
			continue
		try:
			value = math.ceil(float(line.split()[-1]))
		except ValueError as err:
			mon.dbg('ERROR:', err)
			continue
		# connections
		if line.startswith('nginx_ingress_controller_nginx_process_connections{'):
			if line.rfind('state="active"') > 0:
				sts['active'] = value
			elif line.rfind('state="reading"') > 0:
				sts['reading'] = value
			elif line.rfind('state="waiting"') > 0:
				sts['waiting'] = value
			elif line.rfind('state="writing"') > 0:
				sts['writing'] = value
		# connections total
		elif line.startswith('nginx_ingress_controller_nginx_process_connections_total{'):
			if line.rfind('state="accepted"') > 0:
				sts['accepted'] = value
			elif line.rfind('state="handled"') > 0:
				sts['handled'] = value
	return sts

def metrics():
	try:
		resp = urlopen(mon.NGINX_METRICS_URL, None, 15)
	except Exception as err:
		mon.log('ERROR:', err)
		sys.exit(9)
	mon.dbg('resp status:', resp.status)
	if resp.status != 200:
		mon.log('ERROR: metrics response status', resp.status)
		sys.exit(8)
	return parse(resp)

def config():
	mon.dbg('config')
	sts = metrics()
	# connections state
	print('multigraph nginx_connections_state')
	print('graph_title Connections state')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number')
	print('graph_scale no')
	print('active.label active')
	print('active.colour COLOUR0')
	print('active.min 0')
	print('reading.label reading')
	print('reading.colour COLOUR1')
	print('reading.min 0')
	print('waiting.label waiting')
	print('waiting.colour COLOUR2')
	print('waiting.min 0')
	print('writing.label writing')
	print('writing.colour COLOUR3')
	print('writing.min 0')
	# connections total
	print('multigraph nginx_connections_total')
	print('graph_title Connections total')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number')
	print('graph_scale no')
	print('accepted.label accepted')
	print('accepted.colour COLOUR0')
	print('accepted.min 0')
	print('handled.label handled')
	print('handled.colour COLOUR1')
	print('handled.min 0')
	# connections total counter
	print('multigraph nginx_connections_total_counter')
	print('graph_title Connections total counter')
	print('graph_args --base 1000 -l 0')
	print('graph_category nginx')
	print('graph_vlabel number per second')
	print('graph_scale no')
	print('accepted.label accepted')
	print('accepted.colour COLOUR0')
	print('accepted.type COUNTER')
	print('accepted.min 0')
	print('handled.label handled')
	print('handled.colour COLOUR1')
	print('handled.type COUNTER')
	print('handled.min 0')
	# cache
	mon.cacheSet('nginx.connections', sts)
	return 0

def report():
	mon.dbg('report')
	sts = mon.cacheGet('nginx.connections')
	if sts is None:
		sts = metrics()
	# connections
	print('multigraph nginx_connections_state')
	print('active.value', sts['active'])
	print('reading.value', sts['reading'])
	print('waiting.value', sts['waiting'])
	print('writing.value', sts['writing'])
	# connections total
	print('multigraph nginx_connections_total')
	print('accepted.value', sts['accepted'])
	print('handled.value', sts['handled'])
	# connections total counter
	print('multigraph nginx_connections_total_counter')
	print('accepted.value', sts['accepted'])
	print('handled.value', sts['handled'])
	return 0

def main():
	try:
		if sys.argv[1] == 'config':
			return config()
	except IndexError:
		pass
	return report()

if __name__ == '__main__':
	sys.exit(main())
