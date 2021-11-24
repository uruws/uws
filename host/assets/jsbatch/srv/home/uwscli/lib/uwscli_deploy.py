# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from configparser import ConfigParser

import uwscli

_cfgfn = '.uwsci.conf'
_cfgFiles = []

def _newConfig():
	global _cfgFiles
	c = ConfigParser()
	c['DEFAULT'] = {
		'version': 0,
	}
	c['deploy'] = {}
	_cfgFiles = c.read(_cfgfn)
	return c['deploy']

def run(repo, tag):
	uwscli.log('git deploy:', repo, tag)
	cfg = _newConfig()
	return 0
