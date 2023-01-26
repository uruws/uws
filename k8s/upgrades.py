#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import sys

from dataclasses import dataclass
from os          import makedirs
from pathlib     import Path
from shutil      import copytree
from typing      import Callable

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
	# ~ '1.22': Config(
		# ~ docker_tag = '2211',
		# ~ eks_tag    = '122',
		# ~ k8s_tag    = '122',
	# ~ ),
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
	print(name)
	makedirs(name, mode = 0o750, exist_ok = True)

def copy(src: str, dst: str, ignore: Callable = None):
	print(src, '->', dst)
	copytree(src, dst, symlinks = True, dirs_exist_ok = True, ignore = ignore)

#
# k8s
#

def docker_k8s_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	return l

def docker_k8s(version: str, cfg: Config):
	src = './k8s/tpl/docker/k8s'
	dst = './docker/k8s/%s' % cfg.k8s_tag.strip()
	mkdir(dst)
	copy(src, dst, ignore = docker_k8s_ignore)

def k8s_autoscaler(version: str, cfg: Config):
	print('k8s/autoscaler:', version)

#
# eks
#

def docker_eks_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	return l

def docker_eks(version: str, cfg: Config):
	print('docker/eks:', version)
	src = './k8s/tpl/docker/eks'
	dst = './docker/eks/%s' % cfg.eks_tag.strip()
	mkdir(dst)
	copy(src, dst, ignore = docker_eks_ignore)

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
