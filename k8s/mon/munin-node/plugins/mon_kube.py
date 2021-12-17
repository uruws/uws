# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import os

from urllib.request import urlopen

import mon

_uwskube_url = 'http://k8s.mon.svc.cluster.local:2800/kube'
UWSKUBE_URL = os.getenv('UWSKUBE_URL', _uwskube_url)

def _get(uri):
	mon.dbg('kube get:', uri)
	try:
		resp = urlopen(uri, None, 15)
	except Exception as err:
		mon.log('ERROR:', err)
		sys.exit(9)
	mon.dbg('kube resp status:', resp.status)
	if resp.status != 200:
		mon.log('ERROR: kube response status', resp.status)
		sys.exit(8)
	return json.loads(resp.read().decode())

def __parse(uri, mods):
	d = _get(uri)
	sts = dict()
	for n in mods.keys():
		mod = mods.get(n)
		sts[n] = mod.parse(d)
	return sts

def __config(uri, mods):
	sts = __parse(uri, mods)
	for n in mods.keys():
		mod = mods.get(n)
		mod.config(sts[n])
	mon.cacheSet(sts, uri)
	return 0

def __report(uri, mods):
	sts = mon.cacheGet(uri)
	if sts is None:
		sts = __parse(uri, mods)
	for n in mods.keys():
		mod = mods.get(n)
		mod.report(sts[n])
	return 0

def __uri(uri):
	return '/'.join([UWSKUBE_URL, uri])

def main(argv, uri, mods):
	uri = __uri(uri)
	try:
		if argv[0] == 'config':
			return __config(uri, mods)
	except IndexError:
		pass
	return __report(uri, mods)
