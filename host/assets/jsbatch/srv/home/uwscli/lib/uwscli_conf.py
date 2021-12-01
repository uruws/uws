# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import getenv

bindir = getenv('UWSCLI_BINDIR', '/srv/home/uwscli/bin')
cmddir = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

deploy_basedir = getenv('UWSCLI_DEPLOY_BASEDIR', '/srv/deploy')

docker_storage = '/srv/docker/lib'
docker_storage_min = 10*1024*1024 # 10G

class App(object):
	def __init__(self, app, cluster = None, desc = None, pod = None, build = None, deploy = None):
		self.app = app
		self.cluster = cluster
		self.desc = desc
		self.pod = pod
		self.build = build
		self.deploy = deploy

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
	'nlp-sentiment-roberta': App(True,
		cluster = 'panoramix',
		desc = 'NLPService - Sentiment Roberta',
		pod = 'nlpsvc/sentiment/roberta',
		build = AppBuild('/srv/deploy/NLPService', 'build.sh'),
		deploy = AppDeploy('nlpsvc-sentiment-roberta'),
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
	'panoramix': {
		'region': 'us-east-1',
	},
}
