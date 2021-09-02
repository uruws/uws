#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import math
import os
import re
import sys

from urllib.request import urlopen

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon
import nginx_conn

parse_re = re.compile(r'^([^{]+)({[^}]+})\s(\S+)$')
line1_re = re.compile(r'{(\w)')
line2_re = re.compile(r',(\w)')
line3_re = re.compile(r'(\w)=')
line4_re = re.compile(r'"="')

def parse(resp):
	mon.dbg('parse')
	for line in resp.read().decode().splitlines():
		if line.startswith('#'):
			continue
		elif line == '':
			continue
		m = parse_re.match(line)
		if m:
			name = m.group(1)
			ml = m.group(2)
			ml = line1_re.sub(r'{"\1', ml)
			ml = line2_re.sub(r',"\1', ml)
			ml = line3_re.sub(r'\1"=', ml)
			ml = line4_re.sub(r'":"', ml)
			try:
				meta = json.loads(ml)
			except Exception as err:
				mon.log(f"ERROR json {name}:", err)
				mon.dbg('LINE:', ml)
				continue
			try:
				value = math.ceil(float(m.group(3)))
			except ValueError as err:
				mon.dbg(f"ERROR math {name}:", err)
				value = 'U'
		else:
			continue
		# connections
		if name == 'nginx_ingress_controller_nginx_process_connections':
			nginx_conn.parse(meta, value)
		# connections total
		elif name == 'nginx_ingress_controller_nginx_process_connections_total':
			nginx_conn.parse(meta, value)
	return dict(
		nginx_conn = nginx_conn.sts,
	)

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
	# connections
	nginx_conn.config()
	# cache
	mon.cacheSet(sts)
	return 0

def report():
	mon.dbg('report')
	sts = mon.cacheGet()
	if sts is None:
		sts = metrics()
	# connections
	nginx_conn.report(sts['nginx_conn'])
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
