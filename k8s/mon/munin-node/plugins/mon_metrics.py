# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import re
import sys

from urllib.request import urlopen

import mon

# metrics parser

parse_re = re.compile(r'^([^{]+)({[^}]+}\s|\s)(\S+)$')
line1_re = re.compile(r'{(\w)')
line2_re = re.compile(r',(\w)')
line3_re = re.compile(r'(\w)=')
line4_re = re.compile(r'"="')

def _metrics_parse(resp):
	mon.dbg('metrics parse')
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
					mon.log(f"ERROR: json {name}:", err)
					mon.dbg('LINE:', ml)
					continue
			try:
				value = float(m.group(3))
			except ValueError as err:
				mon.dbg(f"float {name}:", err)
		else:
			mon.dbg('metrics parse miss:', line)
			continue
		yield (name, meta, value)

def _exit(rc):
	sys.exit(rc)

def __metrics_get(url):
	mon.dbg('metrics get')
	try:
		resp = urlopen(url, None, 15)
	except Exception as err:
		mon.log('ERROR:', err)
		_exit(9)
	mon.dbg('resp status:', resp.status)
	if resp.status != 200:
		mon.log('ERROR: metrics response status', resp.status)
		_exit(8)
	return _metrics_parse(resp)

# module parse

def __metrics(url, mods):
	mon.dbg('metrics')
	sts = dict()
	for name, meta, value in __metrics_get(url):
		for modname in mods.keys():
			mod = mods.get(modname)
			if mod.parse(name, meta, value):
				mon.dbg('mod parse:', modname)
				continue
	for modname in mods.keys():
		mod = mods.get(modname)
		sts[modname] = mod.sts.copy()
	return sts

# module config

def __config(url, mods):
	mon.dbg('config')
	sts = __metrics(url, mods)
	for modname in mods.keys():
		mod = mods.get(modname)
		mon.dbg('mod config:', modname)
		mod.config(sts[modname])
	mon.cacheSet(sts, url)
	return 0

# module report

def __report(url, mods):
	mon.dbg('report')
	sts = mon.cacheGet(url)
	if sts is None:
		sts = __metrics(url, mods)
	for modname in mods.keys():
		mod = mods.get(modname)
		mon.dbg('mod report:', modname)
		mod.report(sts[modname])
	return 0

# main

def main(argv, url, mods):
	try:
		if argv[0] == 'config':
			return __config(url, mods)
	except IndexError:
		pass
	return __report(url, mods)
