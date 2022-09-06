#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

__doc__ = 'uwsapp users auth'

import json

from argparse import ArgumentParser
from os       import unlink

import uwscli

from uwscli_auth import User
from uwscli_user import AppUser

def _apps_build(user: User) -> dict[str, str]:
	d = dict()
	for app in uwscli.build_list(user = user):
		d[app] = uwscli.app[app].info()
	return d

def _apps_deploy(user: User) -> dict[str, str]:
	d = dict()
	for app in uwscli.deploy_list(user = user):
		d[app] = uwscli.app[app].info()
	return d

def _json_dump(fn: str, data: dict[str, str]):
	with open(fn, 'w') as fh: # pragma: no cover
		json.dump(data, fh)

def _install(uid: str, name: str, data: dict[str, str]) -> int:
	fn = '/run/uwscli/auth/%s/%s.json' % (uid, name)
	newfn = '%s.new' % fn
	_json_dump(newfn, data)
	rc = uwscli.system('/usr/bin/install -v -m 0640 -o uws -g uws %s %s' % (newfn, fn))
	try:
		unlink(newfn)
	except FileNotFoundError:
		pass
	return rc

def main(argv: list[str] = []) -> int:
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	args = flags.parse_args(argv)

	for user in uwscli.user_list():
		username = user.username.strip()
		if username == '': continue
		uid: str = uwscli.user_uuid(username)

		# user remove
		if user.remove:
			uwscli.system('/usr/bin/rm -rf /run/uwscli/auth/%s' % uid)
			continue

		# user dir to save password
		rc = uwscli.system('/usr/bin/install -v -d -m 0750 -o uws -g uws /run/uwscli/auth/%s' % uid)
		if rc != 0: return rc

		# user info file
		u = User(user.name)

		if u.load_groups() != 0: # pragma: no cover
			uwscli.error('could not load user groups:', username, user.name)
			continue

		# user metadata
		d = {
			'uid':         uid,
			'name':        user.name,
			'username':    username,
			'is_operator': user.is_operator,
			'is_admin':    user.is_admin,
		}
		rc = _install(uid, 'meta', d)
		if rc != 0: return rc

		# user apps
		d = {
			'uid':           uid,
			'build_command': 'app-build',
			'commands':      uwscli.user_commands(user),
			'build':         _apps_build(u),
			'deploy':        _apps_deploy(u),
		}
		rc = _install(uid, 'apps', d)
		if rc != 0: return rc

	return 0

if __name__ == '__main__': # pragma: no cover
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
