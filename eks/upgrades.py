#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import subprocess
import sys

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
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
	docker_tag: str       = ''
	rm_tags:    list[str] = field(default_factory = list)
	eks_tag:    str       = ''
	k8s_tag:    str       = ''
	eksctl:     str       = ''

	def eksctl_url(c):
		return 'https://github.com/weaveworks/eksctl/releases/download/v%s' % c.eksctl

# eksctl
#   https://github.com/weaveworks/eksctl/tags

cfg: dict[str, Config] = {
	'1.24': Config(
		docker_tag = '2305',
		rm_tags    = ['2211'],
		eks_tag    = '124',
		k8s_tag    = '124',
	),
}

cfg_remove: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		eks_tag    = '122',
	),
}

def getcfg(v: str, remove = False) -> Config:
	c = None
	if remove:
		c = cfg_remove[v]
	else:
		c = cfg[v]
		loadcfg(v, c)
	return c

def loadcfg(v: str, c: Config):
	if c is None:
		return
	utils = getutils()
	c.eksctl = utils[v]["eksctl"]

def getutils() -> dict[str, dict[str, str]]:
	d = {}
	with Path('./eks/utils.json').open() as fh:
		d = json.load(fh)
	return d

#
# utils
#

def mkdir(name: str):
	# ~ print(name)
	makedirs(name, mode = 0o750, exist_ok = True)

def copy(src: str, dst: str, ignore: Callable = None):
	# ~ print(src, '->', dst)
	copytree(src, dst, symlinks = True, dirs_exist_ok = True, ignore = ignore)

def envsubst(src: str, dst: str, env: dict[str, str]):
	# ~ print(src, '->', dst)
	cmd = ['/usr/bin/envsubst']
	with open(src, 'rb') as stdin:
		with open(dst, 'wb') as stdout:
			subprocess.run(cmd, stdin = stdin, stdout = stdout, env = env, check = True)

def gitrm(path: str):
	if Path(path).exists():
		cmd = ['/usr/bin/git', 'rm', '-rf', path]
		subprocess.run(cmd, check = True)

#
# docker
#

def docker_eks_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	if 'Dockerfile.devel' in names:
		l.append('Dockerfile.devel')
	return l

def docker_version() -> str:
	return Path('./docker/VERSION').read_text().strip()

def docker_eks(version: str, cfg: Config):
	# ~ print('docker/eks:', version)
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
		print('', file = fh)
		print('''RUN printf 'export PS1="${AWS_PROFILE}@\H:\W\$ "\\n' >>.profile''', file = fh)
		print('', file = fh)
		print('CMD exec /usr/local/bin/uws-login.sh', file = fh)

def docker_eks_devel(version: str, cfg: Config):
	srcfn = './eks/tpl/docker/Dockerfile.devel'
	dstfn = './docker/eks/Dockerfile.devel'
	env = {
		'DOCKER_TAG':     cfg.docker_tag.strip(),
		'DOCKER_VERSION': docker_version(),
		'EKS_TAG':        cfg.eks_tag.strip(),
	}
	envsubst(srcfn, dstfn, env)

def docker_eks_cleanup(version: str, cfg: Config):
	eks_tag = cfg.eks_tag.strip()
	gitrm(f"./docker/eks/{eks_tag}")

def docker_eks_build(cfg: dict[str, Config]) -> int:
	buildfn = './docker/eks/build.sh'
	# ~ print(buildfn)
	with open(buildfn, 'w') as fh:
		print('#!/bin/sh', file = fh)
		print('set -eu', file = fh)
		print('# remove old', file = fh)
		for version in sorted(cfg_remove.keys()):
			c = getcfg(version, remove = True)
			docker_tag = c.docker_tag.strip()
			eks_tag = c.eks_tag.strip()
			print(f"# {version}", file = fh)
			print(f"docker rmi uws/eks-{eks_tag}-{docker_tag} || true", file = fh)
		print('# cleanup', file = fh)
		for version in sorted(cfg.keys()):
			c = getcfg(version)
			eks_tag = c.eks_tag.strip()
			print(f"# {version}", file = fh)
			for rmtag in sorted(c.rm_tags):
				print(f"docker rmi uws/eks-{eks_tag}-{rmtag} || true", file = fh)
		print('# build', file = fh)
		for version in sorted(cfg.keys()):
			c = getcfg(version)
			print(f"# {version}", file = fh)
			docker_tag = c.docker_tag.strip()
			eks_tag = c.eks_tag.strip()
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
	if '-i' in argv:
		return show_info()
	latest = 'None'
	for v in sorted(cfg.keys()):
		c = getcfg(v)
		docker_eks(v, c)
		latest = v
	c = getcfg(latest)
	docker_eks_devel(latest, c)
	for v in sorted(cfg_remove.keys()):
		c = getcfg(v, remove = True)
		docker_eks_cleanup(v, c)
	return docker_eks_build(cfg)

def show_info():
	print('Config:')
	for v in sorted(cfg.keys()):
		c = getcfg(v)
		print(' ', v, asdict(c))
	print()
	print('Config remove:')
	for v in sorted(cfg_remove.keys()):
		c = getcfg(v, remove = True)
		print(' ', v, asdict(c))
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
