#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import re
import subprocess
import sys
import yaml

from dataclasses import dataclass
from datetime    import datetime
from os          import chmod
from os          import makedirs
from pathlib     import Path
from shutil      import copytree
from typing      import Any
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
	kubeshark:  str = ''
	autoscaler: str = ''

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

# k8s/autoscaler
#   https://github.com/kubernetes/autoscaler/tags

cfg: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		k8s_tag    = '122',
		kubectl    = '1.22.6/2022-03-09',
		helm       = '3.11.0',
		kubeshark  = '38.5',
		autoscaler = '1.22.2',
	),
	'1.24': Config(
		docker_tag = '2211',
		k8s_tag    = '124',
		kubectl    = '1.24.6/2022-10-05',
		helm       = '3.11.0',
		kubeshark  = '38.5',
		autoscaler = '1.24.0',
	),
}

cfg_remove: dict[str, Config] = {
	'1.25': Config(
		docker_tag = '2211',
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

def envsubst(src: str, dst: str, env: dict[str, str]):
	print(src, '->', dst)
	cmd = '/usr/bin/envsubst'
	with open(src, 'rb') as stdin:
		with open(dst, 'wb') as stdout:
			subprocess.run([cmd], stdin = stdin, stdout = stdout, env = env, check = True)

def gitrm(path: str):
	if Path(path).exists():
		cmd = ['/usr/bin/git', 'rm', '-rf', path]
		subprocess.run(cmd, check = True)

#
# docker
#

def docker_k8s_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
	if 'Dockerfile.devel' in names:
		l.append('Dockerfile.devel')
	return l

def docker_version() -> str:
	now = datetime.now()
	return now.strftime('%y%m%d')

def docker_k8s(version: str, cfg: Config):
	src = './k8s/tpl/docker'
	dst = './docker/k8s/%s' % cfg.k8s_tag.strip()
	mkdir(dst)
	copy(src, dst, ignore = docker_k8s_ignore)
	srcfn = './k8s/tpl/docker/Dockerfile'
	dstfn = './docker/k8s/%s/Dockerfile.%s' % (cfg.k8s_tag.strip(), cfg.docker_tag.strip())
	env = {
		'DOCKER_TAG':     cfg.docker_tag.strip(),
		'DOCKER_VERSION': docker_version(),
		'KUBECTL_URL':    cfg.kubectl_url(),
		'HELM_URL':       cfg.helm_url(),
		'KUBESHARK_URL':  cfg.kubeshark_url(),
	}
	envsubst(srcfn, dstfn, env)

def docker_k8s_devel(version: str, cfg: Config):
	srcfn = './k8s/tpl/docker/Dockerfile.devel'
	dstfn = './docker/k8s/Dockerfile.devel'
	env = {
		'DOCKER_TAG':     cfg.docker_tag.strip(),
		'DOCKER_VERSION': docker_version(),
		'K8S_TAG':        cfg.k8s_tag.strip(),
	}
	envsubst(srcfn, dstfn, env)

def docker_k8s_cleanup(version: str, cfg: Config):
	k8s_tag = cfg.k8s_tag.strip()
	gitrm(f"./docker/k8s/{k8s_tag}")

def docker_k8s_build(cfg: dict[str, Config]) -> int:
	buildfn = './docker/k8s/build.sh'
	print(buildfn)
	with open(buildfn, 'w') as fh:
		print('#!/bin/sh', file = fh)
		print('set -eu', file = fh)
		print('# remove old', file = fh)
		for version in sorted(cfg_remove.keys()):
			docker_tag = cfg_remove[version].docker_tag.strip()
			k8s_tag = cfg_remove[version].k8s_tag.strip()
			print(f"# {version}", file = fh)
			print(f"docker rmi uws/k8s-{k8s_tag}-{docker_tag} || true", file = fh)
		print('# build', file = fh)
		for version in sorted(cfg.keys()):
			print(f"# {version}", file = fh)
			docker_tag = cfg[version].docker_tag.strip()
			k8s_tag = cfg[version].k8s_tag.strip()
			print(f"rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/{k8s_tag}/build/", file = fh)
			print(f"# k8s-{k8s_tag}-{docker_tag}", file = fh)
			print(f"docker build --rm -t uws/k8s-{k8s_tag}-{docker_tag} \\", file = fh)
			print(f"    -f docker/k8s/{k8s_tag}/Dockerfile.{docker_tag} \\", file = fh)
			print(f"    ./docker/k8s/{k8s_tag}", file = fh)
		print('exit 0', file = fh)
	chmod(buildfn, 0o750)
	return 0

#
# k8s tools
#

def k8s_autoscaler_img(v: str, s: str) -> str:
	return re.sub(r':v\d.*$', ':v%s' % v, s)

def k8s_container_command(version: str, cfg: Config, d: dict[str, Any]):
	cmd = []
	for a in d['spec']['template']['spec']['containers'][0]['command']:
		x = a.strip()
		if x.startswith('--node-group-auto-discovery='):
			x = x.replace('<YOUR CLUSTER NAME>', '${UWS_CLUSTER}')
		cmd.append(x)
	d['spec']['template']['spec']['containers'][0]['command'].clear()
	d['spec']['template']['spec']['containers'][0]['command'].extend(cmd)

def k8s_autoscaler(version: str, cfg: Config):
	dstdir = './k8s/autoscaler/%s' % version
	mkdir(dstdir)
	dstfn = '%s/deploy.yaml' % dstdir
	cmd = ['./k8s/autoscaler/upstream-get.sh', cfg.autoscaler]
	with open(dstfn, 'wb') as stdout:
		subprocess.run(cmd, stdout = stdout)
	docs_final = []
	with open(dstfn, 'r') as fh:
		docs = yaml.safe_load_all(fh)
		for d in docs:
			kind = d.get('kind', '')
			if kind == 'Deployment':
				# container image
				img = d['spec']['template']['spec']['containers'][0]['image']
				d['spec']['template']['spec']['containers'][0]['image'] = k8s_autoscaler_img(cfg.autoscaler, img)
				# certs bundle mount path
				d['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = '/etc/ssl/certs/ca-bundle.crt'
				# container command
				k8s_container_command(version, cfg, d)
			docs_final.append(d)
	print(dstfn)
	with open(dstfn, 'w') as fh:
		yaml.safe_dump_all(docs_final, fh, sort_keys = False)

def k8s_autoscaler_cleanup(version: str, cfg: Config):
	gitrm(f"./k8s/autoscaler/{version}")

def k8smon_publish(cfg: Config):
	script = './k8s/mon/publish.sh'
	print(script)
	with open(script, 'w') as fh:
		print('#!/bin/sh', file = fh)
		print('set -eu', file = fh)
		print('MON_TAG=$(cat ./k8s/mon/VERSION)', file = fh)
		print('./docker/ecr-login.sh us-east-1', file = fh)
		for version in sorted(cfg.keys()):
			k8s_tag = cfg[version].k8s_tag.strip()
			docker_tag = cfg[version].docker_tag.strip()
			print(f"# {version}", file = fh)
			print(f"./cluster/ecr-push.sh us-east-1 uws/k8s-{k8s_tag}-{docker_tag} \"uws:mon-k8s-{k8s_tag}-${{MON_TAG}}\"", file = fh)
		print('exit 0', file = fh)
	cmd = ['/usr/bin/shellcheck', script]
	subprocess.run(cmd, check = True)

#
# main
#

def main(argv: list[str]) -> int:
	latest = 'None'
	for v in sorted(cfg.keys()):
		docker_k8s(v, cfg[v])
		k8s_autoscaler(v, cfg[v])
		latest = v
	docker_k8s_devel(latest, cfg[latest])
	for v in sorted(cfg_remove.keys()):
		docker_k8s_cleanup(v, cfg_remove[v])
		k8s_autoscaler_cleanup(v, cfg_remove[v])
	k8smon_publish(cfg)
	return docker_k8s_build(cfg)

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
