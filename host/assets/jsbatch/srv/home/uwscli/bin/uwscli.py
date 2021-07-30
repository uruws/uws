# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import path, system, getenv

bindir = path.abspath(path.dirname(__file__))
cmddir = getenv('UWSCLI_CMDDIR', '/srv/uws/deploy/cli')

class App(object):
	def __init__(self, app, cluster = None, desc = None, pod = None, build = None, actions = []):
		self.app = app
		self.cluster = cluster
		self.desc = desc
		self.pod = pod
		self.build = build
		self.actions = actions

class AppBuild(object):
	def __init__(self, dir, script, image, filter = None):
		self.dir = dir
		self.script = script
		self.image = image
		self.filter = filter
		if self.filter is None:
			self.filter = "%s-" % image

app = {
	'app': App(False,
		desc = 'App web and workers',
		build = AppBuild('/srv/deploy/Buildpack', 'build.py', 'meteor-app'),
	),
	'app-east': App(True,
		cluster = 'amy-east',
		desc = 'App web, east cluster',
		pod = 'meteor/web',
		actions = ['deploy'],
	),
	'app-west': App(True,
		cluster = 'amy-west',
		desc = 'App web, west cluster',
		pod = 'meteor/web',
		actions = ['deploy'],
	),
	'worker': App(True,
		cluster = 'amy-wrkr',
		desc = 'App worker',
		pod = 'meteor/worker',
		actions = ['deploy'],
	),
	'beta': App(True,
		cluster = 'amybeta',
		desc = 'App beta',
		pod = 'meteor/beta',
		build = AppBuild('/srv/deploy/Buildpack', 'build.py', 'meteor-app-beta',
			filter = 'meteor-app-'),
		actions = ['deploy'],
	),
	'cs': App(True,
		cluster = 'amybeta',
		desc = 'Crowdsourcing',
		pod = 'meteor/cs',
		build = AppBuild('/srv/deploy/Buildpack', 'build.py', 'meteor-crowdsourcing'),
		actions = ['deploy'],
	),
	'nlp': App(False,
		cluster = 'panoramix',
		desc = 'NLP: api, ner and sentiment',
		build = AppBuild('/srv/deploy/NLP', 'build.sh', 'nlp-api'),
		pod = 'nlp',
		actions = ['deploy'],
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

def app_list(action = ''):
	return sorted([n for n in app.keys() if (action == '' and app[n].app) or action in app[n].actions])

def app_description(action = ''):
	m = __descmax(app_list(action))
	d = 'available apps:\n'
	for n in app_list(action):
		d += "  %s%s- %s\n" % (n, __descsep(n, m), app[n].desc)
	return d

def build_list():
	return sorted([n for n in app.keys() if app[n].build is not None])

def build_description():
	m = __descmax(build_list())
	d = 'available apps:\n'
	for n in build_list():
		d += "  %s%s- %s\n" % (n, __descsep(n, m), app[n].desc)
	return d

def nq(cmd, args, cmddir = cmddir):
	return system("%s/uwsnq %s/%s %s" % (bindir, cmddir, cmd, args))

def run(cmd, args):
	return system("%s/%s %s" % (cmddir, cmd, args))
