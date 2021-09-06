# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import math
import os
import re
import sys

from time import time
from urllib.request import urlopen

# logger

__debug = os.getenv('UWS_DEBUG', None)

def log(*args):
	print(*args, file = sys.stderr)

def dbg(*args):
	if __debug:
		print('DEBUG: ', end = '', file = sys.stderr)
		log(*args)

# utils

__field_re = re.compile('\W')

def cleanfn(n):
	return __field_re.sub('_', n)

__cachefn = '/tmp/mon.cache.nginx.stats'

# cache

def __cacheSet(obj):
	try:
		obj['__cache_expire'] = time() + 120
		with open(__cachefn, 'w') as fh:
			json.dump(obj, fh)
			fh.close()
	except Exception as err:
		log('ERROR cacheSet:', err)

def __cacheGet():
	obj = None
	try:
		with open(__cachefn, 'r') as fh:
			obj = json.load(fh)
			fh.close()
	except Exception as err:
		log('ERROR cacheGet:', err)
		dbg('cache miss')
		return None
	if obj is not None and time() >= obj['__cache_expire']:
		dbg('cache expired')
		return None
	dbg('cache hit')
	return obj

# metrics parser

parse_re = re.compile(r'^([^{]+)({[^}]+}\s|\s)(\S+)$')
line1_re = re.compile(r'{(\w)')
line2_re = re.compile(r',(\w)')
line3_re = re.compile(r'(\w)=')
line4_re = re.compile(r'"="')

def __metrics_parse(resp):
	dbg('metrics parse')
	for line in resp.read().decode().splitlines():
		if line.startswith('#'):
			continue
		elif line == '':
			continue
		name = None
		meta = None
		value = 'U'
		m = parse_re.match(line)
		if m:
			name = m.group(1)
			ml = m.group(2).strip()
			if ml != '':
				ml = line1_re.sub(r'{"\1', ml)
				ml = line2_re.sub(r',"\1', ml)
				ml = line3_re.sub(r'\1"=', ml)
				ml = line4_re.sub(r'":"', ml)
				try:
					meta = json.loads(ml)
				except Exception as err:
					log(f"ERROR: json {name}:", err)
					dbg('LINE:', ml)
					continue
			try:
				value = math.ceil(float(m.group(3)))
			except ValueError as err:
				dbg(f"math {name}:", err)
		else:
			dbg('metrics parse miss:', line)
			continue
		yield (name, meta, value)

def __metrics_get(url):
	dbg('metrics get')
	try:
		resp = urlopen(url, None, 15)
	except Exception as err:
		log('ERROR:', err)
		sys.exit(9)
	dbg('resp status:', resp.status)
	if resp.status != 200:
		log('ERROR: metrics response status', resp.status)
		sys.exit(8)
	return __metrics_parse(resp)

# module parse

def __metrics(url, mods):
	dbg('metrics')
	sts = dict()
	for name, meta, value in __metrics_get(url):
		for modname in mods.keys():
			mod = mods.get(modname)
			if mod.parse(name, meta, value):
				dbg('mod parse:', modname)
				continue
	for modname in mods.keys():
		mod = mods.get(modname)
		sts[modname] = mod.sts.copy()
	return sts

# module config

def __config(url, mods):
	dbg('config')
	sts = __metrics(url, mods)
	for modname in mods.keys():
		mod = mods.get(modname)
		dbg('mod config:', modname)
		mod.config(sts[modname])
	__cacheSet(sts)
	return 0

# module report

def __report(url, mods):
	dbg('report')
	sts = __cacheGet()
	if sts is None:
		sts = __metrics(url, mods)
	for modname in mods.keys():
		mod = mods.get(modname)
		dbg('mod report:', modname)
		mod.report(sts[modname])
	return 0

# main

def main(url, mods):
	try:
		if sys.argv[1] == 'config':
			return __config(url, mods)
	except IndexError:
		pass
	return __report(url, mods)
