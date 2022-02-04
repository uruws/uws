# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass
from dataclasses import field
from os import getenv

from typing import Optional

bindir: str = getenv('UWSCLI_BINDIR', '/srv/home/uwscli/bin')
cmddir: str = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

deploy_basedir: str = getenv('UWSCLI_DEPLOY_BASEDIR', '/srv/deploy')

docker_storage:     str = '/srv/docker/lib'
docker_storage_min: int = 10*1024*1024 # 10G

@dataclass
class AppBuild(object):
	dir:    str
	script: str
	type:   str = 'cli'
	src:    str = '.'
	target: str = 'None'
	clean:  str = ''

@dataclass
class AppDeploy(object):
	image:  str
	filter: str = ''

	def __post_init__(self):
		if self.filter == '':
			self.filter = "%s-" % self.image

@dataclass
class App(object):
	app:              bool      = False
	cluster:          str       = 'None'
	desc:             str       = 'None'
	pod:              str       = 'None'
	build:            AppBuild  = AppBuild('', '')
	deploy:           AppDeploy = AppDeploy('')
	autobuild:        bool      = False
	autobuild_deploy: list[str] = field(default_factory = list)

def _buildpack(src: str, target: str) -> AppBuild:
	return AppBuild(
		'/srv/deploy/Buildpack',
		'build.py',
		type = 'pack',
		src = src,
		target = target,
		clean = target,
	)

app: dict[str, App] = {
	'app': App(False,
		desc = 'App web and workers',
		build = _buildpack('app/src', 'app'),
		autobuild = True,
		autobuild_deploy = ['app-test-1', 'app-test-2'],
	),
	'app-east': App(True,
		cluster = 'amy-east',
		desc = 'App web, east cluster',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
	),
	'app-west': App(True,
		cluster = 'amy-west',
		desc = 'App web, west cluster',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
	),
	'worker': App(True,
		cluster = 'amy-wrkr',
		desc = 'App worker',
		pod = 'meteor/worker',
		deploy = AppDeploy('meteor-app'),
	),
	'app-test-1': App(True,
		cluster = 'amy-test-1',
		desc = 'App web, test cluster (east)',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
	),
	'app-test-2': App(True,
		cluster = 'amy-test-2',
		desc = 'App web, test cluster (west)',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
	),
	'beta': App(True,
		cluster = 'amybeta',
		desc = 'App beta',
		pod = 'meteor/beta',
		build = _buildpack('beta/src', 'beta'),
		deploy = AppDeploy('meteor-beta'),
	),
	'cs': App(True,
		cluster = 'amybeta',
		desc = 'Crowdsourcing',
		pod = 'meteor/cs',
		build = _buildpack('cs/src', 'crowdsourcing'),
		deploy = AppDeploy('meteor-crowdsourcing'),
	),
	'nlpsvc': App(False,
		desc = 'NLPService',
		build = AppBuild('/srv/deploy/NLPService', 'build.sh', clean = 'nlpsvc'),
	),
	'nlp-sentiment-twitter': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Sentiment Twitter',
		pod = 'nlpsvc/sentiment/twitter',
		deploy = AppDeploy('nlpsvc-sentiment-twitter'),
	),
	'nlp-topic-automl': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Topic automl',
		pod = 'nlpsvc/topic/automl',
		deploy = AppDeploy('nlpsvc'),
	),
	'nlp-category': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Category',
		pod = 'nlpsvc/category',
		deploy = AppDeploy('nlpsvc'),
	),
}

cluster: dict[str, dict[str, str]] = {
	'amy-east': {
		'region': 'us-east-1',
	},
	'amy-west': {
		'region': 'us-west-1',
	},
	'amy-wrkr': {
		'region': 'us-east-1',
	},
	'amybeta': {
		'region': 'us-east-2',
	},
	'amy-test-1': {
		'region': 'us-east-2',
	},
	'amy-test-2': {
		'region': 'us-west-2',
	},
	'panoramix': {
		'region': 'us-east-1',
	},
}
