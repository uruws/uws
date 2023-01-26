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

__doc__ = 'eks upgrades helper'

#
# config
#

@dataclass
class Config(object):
	docker_tag: str = ''
	eks_tag:    str = ''

cfg: dict[str, Config] = {
	# ~ '1.22': Config(
		# ~ docker_tag = '2211',
		# ~ eks_tag    = '122',
	# ~ ),
	'1.25': Config(
		docker_tag = '2211',
		eks_tag    = '125',
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
# docker
#

def docker_eks_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	return l

def docker_eks(version: str, cfg: Config):
	print('docker/eks:', version)
	src = './eks/tpl/docker'
	dst = './docker/eks/%s' % cfg.eks_tag.strip()
	mkdir(dst)
	copy(src, dst, ignore = docker_eks_ignore)

#
# main
#

def main(argv: list[str]) -> int:
	for v in sorted(cfg.keys()):
		docker_eks(v, cfg[v])
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
