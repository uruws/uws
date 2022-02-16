# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass
from dataclasses import field
from os import getenv

bindir: str = getenv('UWSCLI_BINDIR', '/srv/home/uwscli/bin')
cmddir: str = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

deploy_basedir: str = getenv('UWSCLI_DEPLOY_BASEDIR', '/srv/deploy')

docker_storage:     str = '/srv/docker/lib'
docker_storage_min: int = 10*1024*1024 # 10G

admin_group:    str = getenv('UWSCLI_ADMIN_GROUP',    'uwsadm')
operator_group: str = getenv('UWSCLI_OPERATOR_GROUP', 'uwsops')

@dataclass
class AppBuild(object):
	dir:    str
	script: str
	type:   str = 'cli'
	src:    str = '.'
	target: str = 'None'
	clean:  str = ''

def _buildpack(src: str, target: str) -> AppBuild:
	return AppBuild(
		'/srv/deploy/Buildpack',
		'build.py',
		type = 'pack',
		src = src,
		target = target,
		clean = target,
	)

@dataclass
class AppDeploy(object):
	image:  str
	filter: str = ''

	def __post_init__(self):
		if self.filter == '':
			self.filter = "%s-" % self.image

@dataclass
class App(object):
	app:              bool
	cluster:          str       = 'None'
	desc:             str       = 'None'
	pod:              str       = 'None'
	build:            AppBuild  = AppBuild('', '')
	deploy:           AppDeploy = AppDeploy('')
	autobuild:        bool      = False
	autobuild_deploy: list[str] = field(default_factory = list)
	groups:           list[str] = field(default_factory = list)

	def __post_init__(self):
		if len(self.groups) == 0:
			self.groups = ['nogroup']

app: dict[str, App] = {
	'app': App(False,
		desc = 'App web and workers',
		build = _buildpack('app/src', 'app'),
		autobuild = True,
		autobuild_deploy = ['app-test-1', 'app-test-2'],
		groups = ['uwsapp_app'],
	),
	'app-east': App(True,
		cluster = 'amy-east',
		desc = 'App web, east cluster',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_app'],
	),
	'app-west': App(True,
		cluster = 'amy-west',
		desc = 'App web, west cluster',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_app'],
	),
	'worker': App(True,
		cluster = 'amy-wrkr',
		desc = 'App worker',
		pod = 'meteor/worker',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_app'],
	),
	'app-test-1': App(True,
		cluster = 'amy-test-1',
		desc = 'App web, test cluster (east)',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_app', 'uwsapp_apptest'],
	),
	'app-test-2': App(True,
		cluster = 'amy-test-2',
		desc = 'App web, test cluster (west)',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_app', 'uwsapp_apptest'],
	),
	'beta': App(True,
		cluster = 'amybeta',
		desc = 'App beta',
		pod = 'meteor/beta',
		build = _buildpack('beta/src', 'beta'),
		deploy = AppDeploy('meteor-beta'),
		groups = ['uwsapp_app'],
	),
	'cs': App(True,
		cluster = 'amybeta',
		desc = 'Crowdsourcing',
		pod = 'meteor/cs',
		build = _buildpack('cs/src', 'crowdsourcing'),
		deploy = AppDeploy('meteor-crowdsourcing'),
		groups = ['uwsapp_cs'],
	),
	'nlpsvc': App(False,
		desc = 'NLPService',
		build = AppBuild('/srv/deploy/NLPService', 'build.sh', clean = 'nlpsvc'),
		groups = ['uwsapp_nlp'],
	),
	'nlp-sentiment-twitter': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Sentiment Twitter',
		pod = 'nlpsvc/sentiment/twitter',
		deploy = AppDeploy('nlpsvc-sentiment-twitter'),
		groups = ['uwsapp_nlp'],
	),
	'nlp-topic-automl': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Topic automl',
		pod = 'nlpsvc/topic/automl',
		deploy = AppDeploy('nlpsvc'),
		groups = ['uwsapp_nlp'],
	),
	'nlp-category': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Category',
		pod = 'nlpsvc/category',
		deploy = AppDeploy('nlpsvc'),
		groups = ['uwsapp_nlp'],
	),
}

@dataclass
class AppCluster(object):
	region: str

cluster: dict[str, AppCluster] = {
	'amy-east':   AppCluster(region = 'us-east-1'),
	'amy-west':   AppCluster(region = 'us-west-1'),
	'amy-wrkr':   AppCluster(region = 'us-east-1'),
	'amybeta':    AppCluster(region = 'us-east-2'),
	'amy-test-1': AppCluster(region = 'us-east-2'),
	'amy-test-2': AppCluster(region = 'us-west-2'),
	'panoramix':  AppCluster(region = 'us-east-1'),
}
