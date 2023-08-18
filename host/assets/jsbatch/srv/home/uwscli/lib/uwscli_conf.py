# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass
from dataclasses import field
from os          import getenv
from typing      import Any

#-------------------------------------------------------------------------------
# config

homedir: str = getenv('UWSCLI_HOMEDIR', '/home')
sbindir: str = getenv('UWSCLI_SBINDIR', '/srv/home/uwscli/sbin')
bindir:  str = getenv('UWSCLI_BINDIR', '/srv/home/uwscli/bin')
cmddir:  str = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

deploy_basedir: str = getenv('UWSCLI_DEPLOY_BASEDIR', '/srv/deploy')

docker_storage:     str = '/srv/docker'
docker_storage_min: int = 10*1024*1024 # 10G

admin_group:    str = getenv('UWSCLI_ADMIN_GROUP',    'uwsadm')
operator_group: str = getenv('UWSCLI_OPERATOR_GROUP', 'uwsops')

#-------------------------------------------------------------------------------
# utils

def _tapo_pod_containers(name: str, ns: str = 'tapo', hpx = False, api = False, cdn = False, worker = False, wrkns = 'tpwrk') -> list[str]:
	l: list[str] = []
	l.append('%s/meteor-%s' % (ns, name))
	if hpx:
		l.append('%s/%shpx-haproxy-ingress' % (ns, ns))
	if api:
		l.append('%s/meteor-api' % ns)
	if cdn:
		l.append('%s/meteor-cdn' % ns)
	if worker:
		l.append('%s/meteor-worker' % wrkns)
	return sorted(l)

def _meteor_pod_containers(name: str, gw: bool = False) -> list[str]:
	l: list[str] = []
	l.append('%s/meteor' % name)
	if gw:
		l.append('%sgw/proxy' % name)
	return sorted(l)

#-------------------------------------------------------------------------------
# app build

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

#-------------------------------------------------------------------------------
# app deploy

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

#-------------------------------------------------------------------------------
# app

@dataclass
class App(object):
	app:                                    bool
	cluster:                                 str = 'None'
	desc:                                    str = 'None'
	pod:                                     str = 'None'
	pod_containers:                    list[str] = field(default_factory = list)
	build:                        AppBuild | Any = None
	build_blacklist:                   list[str] = field(default_factory = list)
	deploy:                      AppDeploy | Any = None
	autobuild:                              bool = False
	autobuild_deploy:                  list[str] = field(default_factory = list)
	groups:                            list[str] = field(default_factory = list)
	custom_deploy: dict[str, list[CustomDeploy]] = field(default_factory = dict)

	def __post_init__(self):
		if len(self.groups) == 0:
			self.groups = ['nogroup']
		if self.build is None:
			self.build = AppBuild('', '')
		if self.deploy is None:
			self.deploy = AppDeploy('')

#-------------------------------------------------------------------------------
# app config

app: dict[str, App] = {
	'app': App(False,
		desc            = 'App web and workers',
		build           = _buildpack('app/src', 'app'),
		build_blacklist = [
			# 2.98.8 was wrongly created in 2.96 times
			'2.98.8',
		],
		autobuild        = True,
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
		groups = ['uwsapp_app'],
	),
	'api-prod': App(True,
		cluster        = 'appweb-2302',
		desc           = 'App api',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_app'],
		pod            = 'meteor/api',
		pod_containers = _meteor_pod_containers('api', gw = True),
	),
	'app-prod': App(True,
		cluster        = 'appweb-2302',
		desc           = 'App web',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_app'],
		pod            = 'meteor/web',
		# ~ pod_containers = _tapo_pod_containers('web', hpx = True),
		pod_containers = _meteor_pod_containers('web', gw = True),
	),
	'appcdn-prod': App(True,
		cluster        = 'appweb-2302',
		desc           = 'App web CDN',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_app'],
		pod            = 'meteor/webcdn',
		pod_containers = _meteor_pod_containers('webcdn', gw = True),
	),
	'worker': App(True,
		cluster        = 'appwrk-2306',
		desc           = 'App worker cluster',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_app'],
		pod            = 'tapo/worker',
		pod_containers = _tapo_pod_containers('worker', ns = 'tpwrk'),
	),
	'api-test': App(True,
		cluster        = 'apptest-2302',
		desc           = 'App api, test cluster',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_apptest'],
		pod            = 'tapo/api',
		pod_containers = _tapo_pod_containers('api'),
	),
	'app-test': App(True,
		cluster        = 'apptest-2302',
		desc           = 'App web, test cluster',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_apptest'],
		pod            = 'tapo/web',
		pod_containers = _tapo_pod_containers('web', hpx = True),
	),
	'appcdn-test': App(True,
		cluster        = 'apptest-2302',
		desc           = 'App web CDN, test cluster',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_apptest'],
		pod            = 'tapo/cdn',
		pod_containers = _tapo_pod_containers('cdn'),
	),
	'worker-test': App(True,
		cluster        = 'apptest-2302',
		desc           = 'App worker, test cluster',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_apptest'],
		pod            = 'tapo/worker',
		pod_containers = _tapo_pod_containers('worker', ns = 'tpwrk'),
	),
	'cs': App(True,
		cluster          = 'appwrk-2306',
		desc             = 'Crowdsourcing',
		build            = _buildpack('cs/src', 'crowdsourcing'),
		deploy           = AppDeploy('meteor-crowdsourcing'),
		groups           = ['uwsapp_crowdsourcing', 'uwsapp_cs'],
		autobuild        = True,
		autobuild_deploy = ['cs-test'],
		pod              = 'meteor/cs',
		pod_containers   = _meteor_pod_containers('cs', gw = True),
	),
	'cs-test': App(True,
		cluster        = 'apptest-2302',
		desc           = 'Crowdsourcing test',
		deploy         = AppDeploy('meteor-crowdsourcing'),
		groups         = ['uwsapp_crowdsourcing', 'uwsapp_cs'],
		pod            = 'meteor/cs',
		pod_containers = _meteor_pod_containers('cs', gw = True),
	),
	'infra-ui': App(False,
		desc             = 'Infra-UI',
		build            = _buildpack('infra-ui/src', 'infra-ui'),
		groups           = ['uwsapp_infra-ui'],
		autobuild        = True,
		autobuild_deploy = ['infra-ui-test'],
	),
	'infra-ui-prod': App(True,
		cluster        = 'appwrk-2306',
		desc           = 'Infra-UI production',
		deploy         = AppDeploy('meteor-infra-ui'),
		groups         = ['uwsapp_infra-ui'],
		pod            = 'meteor/infra-ui',
		pod_containers = _meteor_pod_containers('infra-ui-prod', gw = True),
	),
	'infra-ui-test': App(True,
		cluster        = 'apptest-2302',
		desc           = 'Infra-UI staging',
		deploy         = AppDeploy('meteor-infra-ui'),
		groups         = ['uwsapp_infra-ui'],
		pod            = 'meteor/infra-ui',
		pod_containers = _meteor_pod_containers('infra-ui-test', gw = True),
	),
	'meteor-vanilla': App(True,
		cluster          = 'apptest-2302',
		desc             = 'Meteor Vanilla',
		pod              = 'meteor/vanilla',
		build            = _buildpack('meteor-vanilla/src', 'meteor-vanilla'),
		deploy           = AppDeploy('meteor-vanilla'),
		groups           = ['uwsapp_meteor-vanilla'],
		autobuild        = True,
		autobuild_deploy = ['meteor-vanilla'],
		pod_containers   = _meteor_pod_containers('meteor-vanilla', gw = True),
	),
	'sarmiento': App(True,
		cluster        = 'pnt-2308',
		desc           = 'App sarmiento test env',
		deploy         = AppDeploy('meteor-app'),
		groups         = ['uwsapp_apptest'],
		pod            = 'tapo/srmnt',
		pod_containers = _tapo_pod_containers('web', ns = 'srmnt', hpx = True, api = True, cdn = True, worker = True, wrkns = 'srmntwrk'),
	),
}

#-------------------------------------------------------------------------------
# cluster

@dataclass
class AppCluster(object):
	region: str

cluster: dict[str, AppCluster] = {
	'apptest-2302':  AppCluster(region = 'us-east-2'),
	'appweb-2302':   AppCluster(region = 'us-east-2'),
	'appwrk-2306':   AppCluster(region = 'us-east-1'),
	'pnt-2308':      AppCluster(region = 'us-east-2'),
}
