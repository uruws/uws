# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import path, system, getenv

bindir = path.abspath(path.dirname(__file__))
cmddir = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')
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
	def __init__(self, dir, script, type = 'cli'):
		self.dir = dir
		self.script = script
		self.type = type

class AppDeploy(object):
	def __init__(self, image, filter = None):
		self.image = image
		self.filter = filter
		if self.filter is None:
			self.filter = "%s-" % image

buildpack = AppBuild('/srv/deploy/Buildpack', 'build.py', type = 'pack')

app = {
	'app': App(False,
		desc = 'App web and workers',
		build = buildpack,
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
		build = buildpack,
		deploy = AppDeploy('meteor-beta'),
	),
	'cs': App(True,
		cluster = 'amybeta',
		desc = 'Crowdsourcing',
		pod = 'meteor/cs',
		build = buildpack,
		deploy = AppDeploy('meteor-crowdsourcing'),
	),
	'nlp': App(False,
		cluster = 'panoramix',
		desc = 'NLP: api, ner and sentiment',
		pod = 'nlp',
		build = AppBuild('/srv/deploy/NLP', 'build.sh'),
		deploy = AppDeploy('nlp-api'),
	),
	'nlp-api': App(True,
		cluster = 'panoramix',
		desc = 'NLP api',
		pod = 'nlp/api',
	),
	'nlp-ner': App(True,
		cluster = 'panoramix',
		desc = 'NLP ner',
		pod = 'nlp/ner',
	),
	'nlp-sentiment': App(True,
		cluster = 'panoramix',
		desc = 'NLP sentiment',
		pod = 'nlp/sentiment',
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

def __descmax(k):
	m = 0
	for s in k:
		l = len(s)
		if l > m:
			m = l
	return m

def __descsep(k, m):
	s = ' '
	for i in range(len(k), m):
		s += ' '
	return s

def __desc(apps):
	m = __descmax(apps)
	d = 'available apps:\n'
	for n in apps:
		d += "  %s%s- %s\n" % (n, __descsep(n, m), app[n].desc)
	return d

def app_list():
	return sorted([n for n in app.keys() if app[n].app])

def app_description():
	return __desc(app_list())

def build_list():
	return sorted([n for n in app.keys() if app[n].build is not None])

def build_description():
	return __desc(build_list())

def deploy_list():
	return sorted([n for n in app.keys() if app[n].deploy is not None])

def deploy_description():
	return __desc(deploy_list())

__user = getenv('USER', 'unknown')

def ctl(args):
	return system("/usr/bin/sudo -H -n -u uws -- %s/app-ctl.sh %s %s" % (cmddir, __user, args))

def nq(cmd, args, build_dir):
	return system("%s/uwsnq.sh %s/%s %s" % (cmddir, build_dir, cmd, args))

def run(cmd, args):
	return system("/usr/bin/sudo -H -n -u uws -- %s/%s %s" % (cmddir, cmd, args))
