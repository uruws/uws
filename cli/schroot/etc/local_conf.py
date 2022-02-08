# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# configuration for local testing environment

import uwscli

from uwscli_conf import App, AppBuild, AppDeploy

uwscli.docker_storage_min = 10

uwscli.app = dict()

app: dict[str, App] = {
	'uwspod': App(False,
		desc = 'uwspod tests',
		build = AppBuild('/etc/uws/cli', 'build.sh'),
		autobuild = True,
		autobuild_deploy = ['podtest'],
	),
	'podtest': App(True,
		cluster = 'panoramix',
		desc = 'podtest',
		pod = 'test',
		deploy = AppDeploy('podtest'),
	),
}

uwscli.cluster = dict()

cluster: dict[str, dict[str, str]] = {
	'panoramix': {
		'region': 'us-east-1',
	},
}
