# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import os
import sys

from urllib.request import urlopen

import mon

_uwskube_url = 'http://k8s.mon.svc.cluster.local:2800/kube'
UWSKUBE_URL = os.getenv('UWSKUBE_URL', _uwskube_url)

def _exit(rc):
	sys.exit(rc)

def _get(uri):
	mon.dbg('kube get:', uri)
	try:
		resp = urlopen(uri, None, 180)
	except Exception as err:
		mon.log('ERROR:', err)
		_exit(9)
	mon.dbg('kube resp status:', resp.status)
	if resp.status != 200:
		mon.log('ERROR: kube response status', resp.status)
		_exit(8)
	return json.loads(resp.read().decode())

def _parse(uri, mods):
	mon.dbg('mon_kube parse:', uri)
	d = _get(uri)
	sts = dict()
	for n in mods.keys():
		mon.dbg('mon_kube parse:', n)
		mod = mods.get(n)
		sts[n] = mod.parse(d)
	return sts

def _config(uri, mods):
	sts = _parse(uri, mods)
	for n in mods.keys():
		mon.dbg('mon_kube config:', n)
		mod = mods.get(n)
		mod.config(sts[n])
	mon.cacheSet(sts, uri)
	return 0

def _report(uri, mods):
	sts = mon.cacheGet(uri)
	if sts is None:
		sts = _parse(uri, mods)
	for n in mods.keys():
		mon.dbg('mon_kube report:', n)
		mod = mods.get(n)
		mod.report(sts[n])
	return 0

def _uri(uri):
	return '/'.join([UWSKUBE_URL, uri])

def main(argv, uri, mods):
	uri = _uri(uri)
	mon.dbg('mon_kube:', uri)
	try:
		if argv[0] == 'config':
			return _config(uri, mods)
	except IndexError:
		pass
	return _report(uri, mods)
