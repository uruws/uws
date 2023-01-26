#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import sys

from dataclasses import dataclass
from os          import makedirs

__doc__ = 'k8s upgrades helper'

#
# config
#

@dataclass
class Config(object):
	docker_tag: str = ''
	eks_tag:    str = ''
	k8s_tag:    str = ''

cfg: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		eks_tag    = '122',
		k8s_tag    = '122',
	),
	'1.25': Config(
		docker_tag = '2211',
		eks_tag    = '125',
		k8s_tag    = '125',
	),
}

#
# utils
#

def mkdir(name: str):
	makedirs(name, mode = 0o750, exist_ok = True)
	print(f"{name}: dir created")

#
# k8s
#

def docker_k8s(version: str, cfg: Config):
	print('docker/k8s:', version)

def k8s_autoscaler(version: str, cfg: Config):
	print('k8s/autoscaler:', version)

#
# eks
#

def docker_eks(version: str, cfg: Config):
	print('docker/eks:', version)

#
# main
#

def main(argv: list[str]) -> int:
	for v in sorted(cfg.keys()):
		docker_k8s(v, cfg[v])
		docker_eks(v, cfg[v])
		k8s_autoscaler(v, cfg[v])
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
