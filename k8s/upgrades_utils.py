# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from upgrades_config import Config

# main

def k8sutils_latest(v: str, c: Config):
	print('FIXME: implement k8s utils latest version updater.', __file__)
	autoscaler_latest(v)

# k8s/autoscaler

def autoscaler_latest(v: str):
	# https://github.com/kubernetes/autoscaler/tags
	pass
