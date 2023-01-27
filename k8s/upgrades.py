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
	'1.25': Config(
		docker_tag = '2211',
		k8s_tag    = '125',
		kubectl    = '1.25.5/2023-01-11',
		helm       = '3.11.0',
		kubeshark  = '38.3',
		autoscaler = '1.25.0',
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
			subprocess.run([cmd], stdin = stdin, stdout = stdout, env = env)

#
# docker
#

def docker_k8s_ignore(src, names):
	l = []
	if 'Dockerfile' in names:
		l.append('Dockerfile')
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
		yaml.safe_dump_all(docs_final, fh)

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
