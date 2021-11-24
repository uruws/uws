# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from configparser import ConfigParser
from pathlib import Path

import uwscli

_cfgfn = '.uwsci.conf'
_cfgFiles = []

def _newConfig():
	global _cfgFiles
	c = ConfigParser()
	c['DEFAULT'] = {
		'version': 0,
	}
	c['deploy'] = {
		'ci_dir': '.ci',
	}
	_cfgFiles = c.read(_cfgfn)
	cfg = c['deploy']
	ci_dir = Path(cfg['ci_dir']).resolve()
	assert ci_dir.is_absolute(), f"invalid ci_dir: {ci_dir}"
	assert ci_dir.is_relative_to(Path('./').resolve()), f"invalid ci_dir: {ci_dir}"
	cfg['ci_dir'] = ci_dir.as_posix()
	return cfg

def run(repo, tag):
	uwscli.log('git deploy:', repo, tag)
	cfg = _newConfig()
	return 0
