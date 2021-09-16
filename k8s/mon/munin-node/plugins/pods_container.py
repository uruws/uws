# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

__mods = dict()

def parse(pods):
	mon.dbg('pods_container parse')
	sts = dict()
	for i in pods['items']:
		kind = i['kind']
		if kind != 'Pod':
			continue
		spec = i['spec'].get('containers', [])
		status = i['status'].get('containerStatuses', [])
		m = i['metadata']
		ns = m.get('namespace', None)
		name = m.get('name', None)
		for modname in sorted(__mods.keys()):
			mon.dbg('pods_container parse', modname)
			if not sts.get(modname, None):
				sts[modname] = dict()
			if not sts[modname].get(ns, None):
				sts[modname][ns] = dict()
			mod = __mods.get(modname)
			sts[modname][ns][name] = mod.parse(spec, status)
	return sts

def config(sts):
	mon.dbg('pods_container config')
	for modname in sorted(sts.keys()):
		mon.dbg('pods_container config', modname)
		mod = __mods[modname]
		mod.config(sts[modname])

def report(sts):
	mon.dbg('pods_container report')
	for modname in sorted(sts.keys()):
		mon.dbg('pods_container report', modname)
		mod = __mods[modname]
		mod.report(sts[modname])
