# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from dataclasses import dataclass

#-------------------------------------------------------------------------------
# uwscli

sys.path.insert(0, '/srv/home/uwscli/lib')

import uwscli_conf # type: ignore

#-------------------------------------------------------------------------------
# cluster

class ClusterError(Exception):
	pass

@dataclass
class Cluster(object):
	name:   str
	region: str

def cluster_list() -> list[Cluster]:
	l: list[Cluster] = []
	for name in uwscli_conf.cluster.keys():
		k = uwscli_conf.cluster[name]
		region = k.region.strip()
		l.append(Cluster(name = name, region = region))
	return l

def cluster_info(name: str) -> Cluster:
	k = uwscli_conf.cluster.get(name, '')
	if name == '':
		name = '[empty]'
	if k == '':
		raise ClusterError('%s: cluster not found' % name)
	return Cluster(name = name, region = k.region)

#-------------------------------------------------------------------------------
# app

class AppError(Exception):
	pass

@dataclass
class App(object):
	name:    str
	cluster: str

def app_list() -> list[App]:
	l: list[App] = []
	for name in uwscli_conf.app.keys():
		a = uwscli_conf.app[name]
		if not a.app:
			continue
		cluster = a.cluster.strip()
		l.append(App(name = name, cluster = cluster))
	return l

def app_info(name: str) -> App:
	a = uwscli_conf.app.get(name, '')
	if name == '':
		name = '[empty]'
	if a == '':
		raise AppError('%s: app not found' % name)
	return App(name = name, cluster = a.cluster)
