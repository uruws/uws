# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# configuration for local testing environment

import uwscli

from uwscli_conf import App, AppBuild, AppDeploy, AppCluster

uwscli.docker_storage_min = 10

uwscli.app.clear()

app: dict[str, App] = {
	'uwspod': App(False,
		desc = 'uwspod tests',
		build = AppBuild('/srv/deploy/uwspod', 'build.sh'),
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

uwscli.cluster.clear()

cluster: dict[str, AppCluster] = {
	'panoramix': AppCluster(region = 'us-east-1'),
}
