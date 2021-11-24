# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from configparser import ConfigParser

import uwscli

def _newConfig():
	cfg = ConfigParser()
	cfg['DEFAULT'] = {
		'version': 0,
	}
	cfg['deploy'] = {}
	return cfg['deploy']

def run(repo, tag):
	uwscli.log('git deploy:', repo, tag)
	cfg = _newConfig()
	return 0
