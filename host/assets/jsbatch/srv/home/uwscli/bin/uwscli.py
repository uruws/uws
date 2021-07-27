# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

app = {
	'app': {'desc': 'App'},
	'beta': {'desc': 'App beta'},
	'cs': {'desc': 'Crowdsourcing'},
}

def app_list():
	return sorted(app.keys())

def app_description():
	d = 'available apps:\n'
	for n in app_list():
		d += "  %s\t- %s\n" % (n, app[n]['desc'])
	return d
