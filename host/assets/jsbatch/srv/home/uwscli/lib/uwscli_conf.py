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

def _ghrepo(n: str) -> str:
	return f"git@github.com:TalkingPts/{n}.git"

def buildpack_repo() -> str:
	return _ghrepo('Buildpack')

@dataclass
class AppBuild(object):
	dir:    str
	script: str
	type:   str = 'cli'
	src:    str = '.'
	target: str = 'None'
	clean:  str = ''
	repo:   str = ''

def _buildpack(src: str, target: str, repo: str = '') -> AppBuild:
	_uri = ''
	if repo != '':
		_uri = _ghrepo(repo)
	return AppBuild(
		'/srv/deploy/Buildpack',
		'build.py',
		type = 'pack',
		src = src,
		target = target,
		clean = target,
		repo = _uri,
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

	def info(self) -> dict[str, str]:
		return {
			'desc':    self.desc.strip(),
			'cluster': self.cluster.strip(),
			'pod':     self.pod.strip(),
		}

app: dict[str, App] = {
	'app': App(False,
		desc = 'App web and workers',
		build = _buildpack('app/src', 'app', 'App'),
		autobuild = True,
		autobuild_deploy = [
			'apitest-east', 'apitest-west',
			'apptest-east', 'apptest-west',
			'worker-test',
		],
		groups = ['uwsapp_app'],
	),
	# ~ 'app-east': App(True,
		# ~ cluster = 'app-east-2209',
		# ~ desc = 'App web, east cluster',
		# ~ pod = 'meteor/web',
		# ~ deploy = AppDeploy('meteor-app'),
		# ~ groups = ['uwsapp_app'],
	# ~ ),
	# ~ 'app-west': App(True,
		# ~ cluster = 'app-west',
		# ~ desc = 'App web, west cluster',
		# ~ pod = 'meteor/web',
		# ~ deploy = AppDeploy('meteor-app'),
		# ~ groups = ['uwsapp_app'],
	# ~ ),
	'worker': App(True,
		cluster = 'worker-2209',
		desc = 'App worker large nodes',
		pod = 'meteor/worker',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_app'],
	),
	'apitest-east': App(True,
		cluster = 'apptest-east',
		desc = 'App api, test cluster (east)',
		pod = 'meteor/api',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_apptest'],
	),
	'apitest-west': App(True,
		cluster = 'apptest-west',
		desc = 'App api, test cluster (west)',
		pod = 'meteor/api',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_apptest'],
	),
	'apptest-east': App(True,
		cluster = 'apptest-east',
		desc = 'App web, test cluster (east)',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_apptest'],
	),
	'apptest-west': App(True,
		cluster = 'apptest-west',
		desc = 'App web, test cluster (west)',
		pod = 'meteor/web',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_apptest'],
	),
	'worker-test': App(True,
		cluster = 'apptest-east',
		desc = 'App worker test',
		pod = 'meteor/worker',
		deploy = AppDeploy('meteor-app'),
		groups = ['uwsapp_apptest'],
	),
	# ~ 'beta': App(True,
		# ~ cluster = 'panoramix-2206',
		# ~ desc = 'App beta',
		# ~ pod = 'meteor/beta',
		# ~ build = _buildpack('beta/src', 'beta'),
		# ~ deploy = AppDeploy('meteor-beta'),
		# ~ groups = ['uwsapp_beta'],
	# ~ ),
	'cs': App(True,
		cluster = 'panoramix-2206',
		desc = 'Crowdsourcing',
		pod = 'meteor/cs',
		build = _buildpack('cs/src', 'crowdsourcing', 'Crowdsourcing'),
		deploy = AppDeploy('meteor-crowdsourcing'),
		groups = ['uwsapp_crowdsourcing', 'uwsapp_cs'],
		autobuild = True,
		autobuild_deploy = ['cs-test'],
	),
	'cs-test': App(True,
		cluster = 'apptest-east',
		desc = 'Crowdsourcing test',
		pod = 'meteor/cs',
		deploy = AppDeploy('meteor-crowdsourcing'),
		groups = ['uwsapp_crowdsourcing', 'uwsapp_cs'],
	),
	'nlpsvc': App(False,
		desc = 'NLPService',
		build = AppBuild(
			'/srv/deploy/NLPService',
			'build.sh',
			clean = 'nlpsvc',
			repo = _ghrepo('NLPService'),
		),
		groups = ['uwsapp_nlpsvc', 'uwsapp_nlp'],
	),
	'nlp-sentiment-twitter': App(True,
		cluster = 'panoramix-2206',
		desc = 'NLPService - Sentiment Twitter',
		pod = 'nlpsvc/sentiment/twitter',
		deploy = AppDeploy('nlpsvc-sentiment-twitter'),
		groups = ['uwsapp_nlp'],
	),
	'nlp-category': App(True,
		cluster = 'panoramix-2206',
		desc = 'NLPService - Category',
		pod = 'nlpsvc/category',
		deploy = AppDeploy('nlpsvc'),
		groups = ['uwsapp_nlp'],
	),
	'infra-ui': App(False,
		desc = 'Infra-UI',
		build = _buildpack('infra-ui/src', 'infra-ui', 'Infra-UI'),
		groups = ['uwsapp_infra-ui'],
		autobuild = True,
		autobuild_deploy = ['infra-ui-test'],
	),
	'infra-ui-prod': App(True,
		cluster = 'panoramix-2206',
		desc = 'Infra-UI production',
		pod = 'meteor/infra-ui',
		deploy = AppDeploy('meteor-infra-ui'),
		groups = ['uwsapp_infra-ui'],
	),
	'infra-ui-test': App(True,
		cluster = 'apptest-west',
		desc = 'Infra-UI testing',
		pod = 'meteor/infra-ui',
		deploy = AppDeploy('meteor-infra-ui'),
		groups = ['uwsapp_infra-ui'],
	),
	'meteor-vanilla': App(True,
		cluster = 'apptest-east',
		desc = 'Meteor Vanilla',
		pod = 'meteor/vanilla',
		build = _buildpack('meteor-vanilla/src', 'meteor-vanilla', 'MeteorVanilla'),
		deploy = AppDeploy('meteor-vanilla'),
		groups = ['uwsapp_meteor-vanilla'],
		autobuild = True,
		autobuild_deploy = ['meteor-vanilla'],
	),
}

@dataclass
class AppCluster(object):
	region: str

cluster: dict[str, AppCluster] = {
	# ~ 'app-east-2209':  AppCluster(region = 'us-east-1'),
	# ~ 'app-west':       AppCluster(region = 'us-west-2'),
	'apptest-east':   AppCluster(region = 'us-east-2'),
	'apptest-west':   AppCluster(region = 'us-west-2'),
	'panoramix-2206': AppCluster(region = 'us-east-1'),
	'worker-2209':    AppCluster(region = 'us-east-1'),
}
