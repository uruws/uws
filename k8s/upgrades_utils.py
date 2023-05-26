# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from upgrades_config import Config

# main

def k8sutils_latest(v: str, c: Config):
	autoscaler_latest(v)

# k8s/autoscaler

def autoscaler_latest(v: str):
	# https://github.com/kubernetes/autoscaler/tags
	pass
