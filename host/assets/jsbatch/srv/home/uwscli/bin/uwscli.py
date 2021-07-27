# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import path, system

app = {
	'app': {'desc': 'App'},
	'beta': {'desc': 'App beta'},
	'cs': {'desc': 'Crowdsourcing'},
}

bindir = path.abspath(path.dirname(__file__))
cmddir = '/srv/uws/deploy/cli'

def app_list():
	return sorted(app.keys())

def app_description():
	d = 'available apps:\n'
	for n in app_list():
		d += "  %s\t- %s\n" % (n, app[n]['desc'])
	return d

def nq(cmd, args, cmddir = cmddir):
	return system("%s/uwsnq %s/%s %s" % (bindir, cmddir, cmd, args))
