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
_scriptTtl = 3600

def _newConfig():
	global _cfgFiles
	c = ConfigParser()
	c['DEFAULT'] = {
		'version': 0,
	}
	c['deploy'] = {
		'ci_dir': '.ci',
		'ttl': _scriptTtl,
	}
	_cfgFiles = c.read(_cfgfn)
	cfg = c['deploy']

	ci_dir = Path(cfg['ci_dir']).resolve()
	assert ci_dir.is_absolute(), f"invalid ci_dir: {ci_dir}"
	assert ci_dir.is_relative_to(Path('./').resolve()), f"invalid ci_dir: {ci_dir}"
	cfg['ci_dir'] = ci_dir.as_posix()

	assert isinstance(int(cfg['ttl']), int), f"invalid ttl numer: {cfg['ttl']}"
	return cfg

def _deploy(repo, tag, ci_dir, ttl):
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
			rc = uwscli.system(cmd, env = env, timeout = ttl)
			if rc != 0:
				return rc
	return 0

def _rollback(repo, tag, ci_dir, ttl):
	rc = uwscli.git_checkout(tag)
	if rc == 0:
		_deploy(repo, tag, ci_dir, ttl)
	# TODO: send munin-alert if rollback failed

def run(repo, tag, cur = None, fetch = True, checkout = True):
	uwscli.log('uwscli deploy:', repo, tag)
	# current
	if cur is None:
		cur = uwscli.git_describe()
		uwscli.log('current:', cur)
	# fetch metadata
	if fetch:
		uwscli.log('git fetch')
		rc = uwscli.git_fetch()
		if rc != 0:
			return rc
	# checkout tag
	if checkout:
		uwscli.log('git checkout:', tag)
		rc = uwscli.git_checkout(tag)
		if rc != 0:
			return rc
	# configure
	cfg = _newConfig()
	ci_dir = cfg['ci_dir']
	ttl = int(cfg['ttl'])
	# deploy
	uwscli.log('deploy:', repo, tag, ci_dir)
	rc = _deploy(repo, tag, ci_dir, ttl)
	if rc != 0:
		# rollback
		uwscli.log('rollback:', repo, tag, ci_dir, ttl)
		_rollback(repo, cur, ci_dir, ttl)
		return rc
	return 0
