# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass
from dataclasses import field
from os import getenv

homedir: str = getenv('UWSCLI_HOMEDIR', '/home')
sbindir: str = getenv('UWSCLI_SBINDIR', '/srv/home/uwscli/sbin')
bindir:  str = getenv('UWSCLI_BINDIR', '/srv/home/uwscli/bin')
cmddir:  str = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

deploy_basedir: str = getenv('UWSCLI_DEPLOY_BASEDIR', '/srv/deploy')

docker_storage:     str = '/srv/docker'
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

Buildpack = _buildpack

@dataclass
class AppDeploy(object):
	image:  str
	filter: str = ''

	def __post_init__(self):
		if self.filter == '':
			self.filter = "%s-" % self.image

@dataclass
class CustomDeploy(object):
	app:  str
	wait: str = '5m'

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
	custom_deploy:    dict[str, list[CustomDeploy]] = field(default_factory = dict)

	def __post_init__(self):
		if len(self.groups) == 0:
			self.groups = ['nogroup']

app: dict[str, App] = {
	'app': App(False,
		desc      = 'App web and workers',
		build     = _buildpack('app/src', 'app'),
		groups    = ['uwsapp_app'],
		autobuild = True,
		autobuild_deploy = [
			'worker-test',
			'api-test',
			'app-test',
		],
		custom_deploy = {
			'production': [
				CustomDeploy('worker'),
				CustomDeploy('api-prod'),
				CustomDeploy('app-prod'),
			],
			'staging': [
				CustomDeploy('worker-test'),
				CustomDeploy('api-test'),
				CustomDeploy('app-test'),
			],
		},
	),
	'api-prod': App(True,
		cluster = 'appprod-2302',
		desc    = 'App api',
		pod     = 'meteor/api',
		deploy  = AppDeploy('meteor-app'),
		groups  = ['uwsapp_app'],
	),
	'app-prod': App(True,
		cluster = 'appprod-2302',
		desc    = 'App web',
		pod     = 'meteor/web',
		deploy  = AppDeploy('meteor-app'),
		groups  = ['uwsapp_app'],
	),
	'worker': App(True,
		cluster = 'appwrk-2302',
		desc    = 'App worker cluster',
		pod     = 'meteor/worker',
		deploy  = AppDeploy('meteor-app'),
		groups  = ['uwsapp_app'],
	),
	'api-test': App(True,
		cluster = 'apptest-2302',
		desc    = 'App api, test cluster',
		pod     = 'meteor/api',
		deploy  = AppDeploy('meteor-app'),
		groups  = ['uwsapp_apptest'],
	),
	'app-test': App(True,
		cluster = 'apptest-2302',
		desc    = 'App web, test cluster',
		pod     = 'meteor/web',
		deploy  = AppDeploy('meteor-app'),
		groups  = ['uwsapp_apptest'],
	),
	'worker-test': App(True,
		cluster = 'apptest-2302',
		desc    = 'App worker, test cluster',
		pod     = 'meteor/worker',
		deploy  = AppDeploy('meteor-app'),
		groups  = ['uwsapp_apptest'],
	),
	'cs': App(True,
		cluster   = 'appsprod-2302',
		desc      = 'Crowdsourcing',
		pod       = 'meteor/cs',
		build     = _buildpack('cs/src', 'crowdsourcing'),
		deploy    = AppDeploy('meteor-crowdsourcing'),
		groups    = ['uwsapp_crowdsourcing', 'uwsapp_cs'],
		autobuild = True,
		autobuild_deploy = ['cs-test'],
	),
	'cs-test': App(True,
		cluster = 'apptest-2302',
		desc    = 'Crowdsourcing test',
		pod     = 'meteor/cs',
		deploy  = AppDeploy('meteor-crowdsourcing'),
		groups  = ['uwsapp_crowdsourcing', 'uwsapp_cs'],
	),
	'infra-ui': App(False,
		desc      = 'Infra-UI',
		build     = _buildpack('infra-ui/src', 'infra-ui'),
		groups    = ['uwsapp_infra-ui'],
		autobuild = True,
		# ~ autobuild_deploy = ['infra-ui-test'],
	),
	'infra-ui-prod': App(True,
		cluster = 'appsprod-2302',
		desc    = 'Infra-UI production',
		pod     = 'meteor/infra-ui',
		deploy  = AppDeploy('meteor-infra-ui'),
		groups  = ['uwsapp_infra-ui'],
	),
	'meteor-vanilla': App(True,
		cluster   = 'apptest-2302',
		desc      = 'Meteor Vanilla',
		pod       = 'meteor/vanilla',
		build     = _buildpack('meteor-vanilla/src', 'meteor-vanilla'),
		deploy    = AppDeploy('meteor-vanilla'),
		groups    = ['uwsapp_meteor-vanilla'],
		autobuild = True,
		autobuild_deploy = ['meteor-vanilla'],
	),
}

@dataclass
class AppCluster(object):
	region: str

cluster: dict[str, AppCluster] = {
	'appprod-2302':  AppCluster(region = 'us-east-1'),
	'appsprod-2302': AppCluster(region = 'us-east-1'),
	'apptest-2302':  AppCluster(region = 'us-east-2'),
	'appwrk-2302':   AppCluster(region = 'us-east-2'),
}
