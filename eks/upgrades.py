#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import subprocess
import sys

from dataclasses import dataclass
from datetime    import datetime
from os          import chmod
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
	k8s_tag:    str = ''
	eks_tag:    str = ''
	eksctl:     str = ''

	def eksctl_url(c):
		return 'https://github.com/weaveworks/eksctl/releases/download/v%s' % c.eksctl

# eksctl
#   https://github.com/weaveworks/eksctl/tags

cfg: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		k8s_tag    = '122',
		eks_tag    = '122',
		eksctl     = '0.101.0',
	),
	'1.25': Config(
		docker_tag = '2211',
		k8s_tag    = '125',
		eks_tag    = '125',
		eksctl     = '0.126.0',
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

def envsubst(src: str, dst: str, env: dict[str, str]):
	print(src, '->', dst)
	cmd = ['/usr/bin/envsubst']
	with open(src, 'rb') as stdin:
		with open(dst, 'wb') as stdout:
			subprocess.run(cmd, stdin = stdin, stdout = stdout, env = env, check = True)

#
# docker
#

def docker_eks_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	return l

def docker_version() -> str:
	now = datetime.now()
	return now.strftime('%y%m%d')

def docker_eks(version: str, cfg: Config):
	print('docker/eks:', version)
	src = './eks/tpl/docker'
	dst = './docker/eks/%s' % cfg.eks_tag.strip()
	mkdir(dst)
	copy(src, dst, ignore = docker_eks_ignore)
	srcfn = './eks/tpl/docker/Dockerfile'
	dstfn = './docker/eks/%s/Dockerfile.%s' % (cfg.eks_tag.strip(), cfg.docker_tag.strip())
	env = {
		'DOCKER_TAG':     cfg.docker_tag.strip(),
		'DOCKER_VERSION': docker_version(),
		'K8S_TAG':        cfg.k8s_tag.strip(),
		'EKSCTL_URL':     cfg.eksctl_url(),
	}
	envsubst(srcfn, dstfn, env)
	with open(dstfn, 'a') as fh:
		print('''RUN printf 'export PS1="${AWS_PROFILE}@\H:\W\$ "\\n' >>.profile''', file = fh)
		print('', file = fh)
		print('CMD exec /usr/local/bin/uws-login.sh', file = fh)

def docker_eks_build(cfg: dict[str, Config]) -> int:
	buildfn = './docker/eks/build.sh'
	print(buildfn)
	with open(buildfn, 'w') as fh:
		print('#!/bin/sh', file = fh)
		print('set -eu', file = fh)
		for version in sorted(cfg.keys()):
			print(f"# {version}", file = fh)
			docker_tag = cfg[version].docker_tag.strip()
			eks_tag = cfg[version].eks_tag.strip()
			print(f"# eks-{eks_tag}-{docker_tag}", file = fh)
			print(f"docker build --rm -t uws/eks-{eks_tag}-{docker_tag} \\", file = fh)
			print(f"    -f docker/eks/{eks_tag}/Dockerfile.{docker_tag} \\", file = fh)
			print(f"    ./docker/eks/{eks_tag}", file = fh)
		print('exit 0', file = fh)
	chmod(buildfn, 0o750)
	return 0

#
# main
#

def main(argv: list[str]) -> int:
	for v in sorted(cfg.keys()):
		docker_eks(v, cfg[v])
	return docker_eks_build(cfg)

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
