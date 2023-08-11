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
