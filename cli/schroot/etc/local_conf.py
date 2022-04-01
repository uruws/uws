# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# configuration for local testing environment

import uwscli

from uwscli_conf import App, AppBuild, AppDeploy, AppCluster

uwscli.docker_storage_min = 10

uwscli.app.clear()

uwscli.app['uwspod'] = App(False,
	desc = 'uwspod tests',
	build = AppBuild('/srv/deploy/uwspod', 'build.sh'),
	autobuild = True,
	autobuild_deploy = ['podtest'],
)
uwscli.app['podtest'] = App(True,
	cluster = 'panoramix',
	desc = 'podtest',
	pod = 'test',
	deploy = AppDeploy('podtest'),
)

uwscli.cluster.clear()

uwscli.cluster['panoramix'] = AppCluster(region = 'us-east-1')
