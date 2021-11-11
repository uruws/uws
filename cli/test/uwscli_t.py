# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from io import StringIO

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

def mock():
	uwscli._outfh = None
	uwscli._outfh = StringIO()
	uwscli._errfh = None
	uwscli._errfh = StringIO()
