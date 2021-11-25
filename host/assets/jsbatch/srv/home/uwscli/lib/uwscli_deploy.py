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

def _deploy(repo, tag, ci_dir):
	for idx in sorted(_ciScripts.keys()):
		script = Path(ci_dir, _ciScripts[idx])
		if script.exists() and script.is_file() and not script.is_symlink():
			__, __, repo_name, __, __ = urlsplit(repo)
			env = {
				'UWSCLI_REPO': repo,
				'UWSCLI_REPO_NAME': repo_name,
				'UWSCLI_REPO_TAG': tag,
			}
			cmd = script.as_posix()
			uwscli.log('run:', repo, tag, cmd)
			rc = uwscli.system(cmd, env = env)
			if rc != 0:
				return rc
	return 0

def _rollback(repo, tag, ci_dir):
	rc = uwscli.git_checkout(tag)
	if rc != 0:
		return rc
	_deploy(repo, tag, ci_dir)

def run(repo, tag):
	uwscli.log('git deploy:', repo, tag)
	cur = uwscli.git_describe()
	cfg = _newConfig()
	rc = _deploy(repo, tag, cfg['ci_dir'])
	if rc != 0:
		_rollback(repo, cur, cfg['ci_dir'])
		return rc
	return 0
