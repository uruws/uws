# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import uwscli
import uwscli_conf

uwscli.app['testing'] = uwscli_conf.App(True,
	cluster = 'ktest',
	desc = 'Testing',
	pod = 'test',
	build = uwscli_conf.AppBuild('/srv/deploy/Testing', 'build.sh'),
	deploy = uwscli_conf.AppDeploy('test'),
)

uwscli.cluster['ktest'] = {
	'region': 'testing-1',
}
