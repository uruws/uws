# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# ~ import json
# ~ import re
# ~ import subprocess
# ~ import sys
# ~ import yaml

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
# ~ from os          import chmod
# ~ from os          import makedirs
# ~ from pathlib     import Path
# ~ from shutil      import copytree
# ~ from typing      import Any
# ~ from typing      import Callable

__doc__ = 'k8s upgrades config'

@dataclass
class Config(object):
	docker_tag: str       = ''
	rm_tags:    list[str] = field(default_factory = list)
	k8s_tag:    str       = ''
	kubectl:    str       = ''
	helm:       str       = ''
	kubeshark:  str       = ''
	autoscaler: str       = ''

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
	'1.24': Config(
		docker_tag = '2305',
		rm_tags    = ['2211'],
		k8s_tag    = '124',
	),
}

cfg_remove: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		k8s_tag    = '122',
	),
}
