# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import path, system

bindir = path.abspath(path.dirname(__file__))
cmddir = '/srv/uws/deploy/cli'

app = {
	'app': {
		'desc': 'App',
	},
	'beta': {
		'desc': 'App beta',
	},
	'cs': {
		'desc': 'Crowdsourcing',
	},
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
}

deploy = {
	'app-east': {
		'cluster': 'amy-east',
		'desc': 'App web, east cluster',
		'pod': 'meteor/web',
		'image': {
			'filter': 'meteor-app',
			'strip': 'meteor-app-',
		},
	},
	'app-west': {
		'cluster': 'amy-west',
		'desc': 'App web, west cluster',
		'pod': 'meteor/web',
		'image': {
			'filter': 'meteor-app',
			'strip': 'meteor-app-',
		},
	},
	'worker': {
		'cluster': 'amy-wrkr',
		'desc': 'App worker',
		'pod': 'meteor/worker',
		'image': {
			'filter': 'meteor-app',
			'strip': 'meteor-app-',
		},
	},
	'beta': {
		'cluster': 'amybeta',
		'desc': app['beta']['desc'],
		'pod': 'meteor/beta',
		'image': {
			'filter': 'meteor-beta',
			'strip': 'meteor-',
		},
	},
	'cs': {
		'cluster': 'amybeta',
		'desc': app['cs']['desc'],
		'pod': 'meteor/cs',
		'image': {
			'filter': 'meteor-crowdsourcing',
			'strip': 'meteor-crowdsourcing-',
		},
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

def app_list():
	return sorted(app.keys())

def app_description():
	m = __descmax(app.keys())
	d = 'available apps:\n'
	for n in app_list():
		d += "  %s%s- %s\n" % (n, __descsep(n, m), app[n]['desc'])
	return d

def deploy_list():
	return sorted(deploy.keys())

def deploy_description():
	m = __descmax(deploy.keys())
	d = 'available apps:\n'
	for n in deploy_list():
		d += "  %s%s- %s\n" % (n, __descsep(n, m), deploy[n]['desc'])
	return d

def nq(cmd, args, cmddir = cmddir):
	return system("%s/uwsnq %s/%s %s" % (bindir, cmddir, cmd, args))
