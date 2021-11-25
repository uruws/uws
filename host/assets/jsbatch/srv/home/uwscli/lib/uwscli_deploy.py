# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from configparser import ConfigParser
from pathlib import Path
from urllib.parse import urlsplit

import uwscli

_cfgfn = '.uwsci.conf'
_cfgFiles = []
_ciScripts = {
	0: 'build.sh',
	1: 'check.sh',
	2: 'install.sh',
	3: 'deploy.sh',
	4: 'clean.sh',
}

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

def _run(repo, tag, script):
	if script.exists() and script.is_file() and not script.is_symlink():
		__, __, repo_name, __, __ = urlsplit(repo)
		env = {
			'UWSCLI_REPO': repo,
			'UWSCLI_REPO_NAME': repo_name,
			'UWSCLI_REPO_TAG': tag,
		}
		cmd = script.as_posix()
		uwscli.log('run:', repo, tag, cmd)
		return uwscli.system(cmd, env = env)
	return 0

def run(repo, tag):
	uwscli.log('git deploy:', repo, tag)
	cfg = _newConfig()
	for idx in sorted(_ciScripts.keys()):
		s = Path(cfg['ci_dir'], _ciScripts[idx])
		rc = _run(repo, tag, s)
		if rc != 0:
			return rc
	return 0
