# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import getenv

bindir = getenv('UWSCLI_BINDIR', '/srv/home/uwscli/bin')
cmddir = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

deploy_basedir = getenv('UWSCLI_DEPLOY_BASEDIR', '/srv/deploy')

docker_storage = '/srv/docker/lib'
docker_storage_min = 10*1024*1024 # 10G

class App(object):
	def __init__(self, app, cluster = None, desc = None, pod = None, build = None, deploy = None, autobuild = False, autobuild_deploy = []):
		self.app = app
		self.cluster = cluster
		self.desc = desc
		self.pod = pod
		self.build = build
		self.deploy = deploy
		self.autobuild = autobuild
		self.autobuild_deploy = autobuild_deploy

class AppBuild(object):
	def __init__(self, dir, script, type = 'cli', src = '.', target = None):
		self.dir = dir
		self.script = script
		self.type = type
		self.src = src
		self.target = target

class AppDeploy(object):
	def __init__(self, image, filter = None):
		self.image = image
		self.filter = filter
		if self.filter is None:
			self.filter = "%s-" % image

def _buildpack(src, target):
	return AppBuild(
		'/srv/deploy/Buildpack',
		'build.py',
		type = 'pack',
		src = src,
		target = target,
	)

app = {
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
		build = AppBuild('/srv/deploy/NLPService', 'build.sh'),
	),
	'nlp-sentiment-roberta': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Sentiment Roberta',
		pod = 'nlpsvc/sentiment/roberta',
		deploy = AppDeploy('nlpsvc-sentiment-roberta'),
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

cluster = {
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
