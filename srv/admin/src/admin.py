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
	if k == '':
		raise ClusterError('%s: cluster not found' % name)
	return Cluster(name = name, region = k.region)
