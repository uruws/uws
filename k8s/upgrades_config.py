# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from pathlib     import Path

__doc__ = 'k8s upgrades config'

# kubectl
#   https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#linux
#   https://amazon-eks.s3.us-west-2.amazonaws.com/?versions&prefix=1.25

# helm
#   https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
#   https://github.com/helm/helm/tags

# kubeshark
#   https://docs.kubeshark.co/en/install
#   https://github.com/kubeshark/kubeshark/tags

@dataclass
class Config(object):
	docker_tag: str       = ''
	rm_tags:    list[str] = field(default_factory = list)
	k8s_tag:    str       = ''
	# utils
	autoscaler: str       = ''
	helm:       str       = ''
	kubectl:    str       = ''
	kubeshark:  str       = ''

	def helm_url(c):
		return 'https://get.helm.sh/helm-v%s' % c.helm

	def kubectl_url(c):
		return 'https://amazon-eks.s3.us-west-2.amazonaws.com/%s' % c.kubectl

	def kubeshark_url(c):
		return 'https://github.com/kubeshark/kubeshark/releases/download/%s' % c.kubeshark

def loadcfg(v: str, c: Config):
	if c is None:
		return
	utils = getutils()
	c.autoscaler = utils[v]["autoscaler"]
	c.helm       = utils[v]["helm"]
	c.kubectl    = utils[v]["kubectl"]
	c.kubeshark  = utils[v]["kubeshark"]

def getutils() -> dict[str, dict[str, str]]:
	d = {}
	with Path('./k8s/utils.json').open() as fh:
		d = json.load(fh)
	return d

def getcfg(v: str, remove = False) -> Config:
	c = None
	if remove:
		c = cfg_remove[v]
	else:
		c = cfg[v]
		loadcfg(v, c)
	return c

cfg: dict[str, Config] = {
	'1.24': Config(
		docker_tag = '2309',
		rm_tags    = ['2305'],
		k8s_tag    = '124',
	),
}

cfg_remove: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		k8s_tag    = '122',
	),
}
