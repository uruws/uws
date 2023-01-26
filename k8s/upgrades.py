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
	k8s_tag:    str = ''
	kubectl:    str = ''
	helm:       str = ''
	kubeshark   str = ''

	def kubectl_url(c):
		return 'https://amazon-eks.s3.us-west-2.amazonaws.com/%s' % c.kubectl

	def helm_url(c):
		return 'https://get.helm.sh/helm-v%s' % c.helm

	def kubeshark_url(c):
		return 'https://github.com/kubeshark/kubeshark/releases/download/%s' % c.kubeshark

# kubectl
#   https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#linux
#   https://amazon-eks.s3.us-west-2.amazonaws.com/?versions&prefix=1.25

# helm
#   https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
#   https://github.com/helm/helm/tags

# kubeshark
#   https://docs.kubeshark.co/en/install
#   https://github.com/kubeshark/kubeshark/tags

cfg: dict[str, Config] = {
	# ~ '1.22': Config(
		# ~ docker_tag = '2211',
		# ~ k8s_tag    = '122',
	# ~ ),
	'1.25': Config(
		docker_tag = '2211',
		k8s_tag    = '125',
		kubectl    = '1.25.5/2023-01-11',
		helm       = '3.11.0',
		kubeshark  = '38.3',
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

def docker_k8s_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	return l

def docker_k8s(version: str, cfg: Config):
	src = './k8s/tpl/docker'
	dst = './docker/k8s/%s' % cfg.k8s_tag.strip()
	mkdir(dst)
	copy(src, dst, ignore = docker_k8s_ignore)

#
# k8s tools
#

def k8s_autoscaler(version: str, cfg: Config):
	print('k8s/autoscaler:', version)

#
# main
#

def main(argv: list[str]) -> int:
	for v in sorted(cfg.keys()):
		docker_k8s(v, cfg[v])
		k8s_autoscaler(v, cfg[v])
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
