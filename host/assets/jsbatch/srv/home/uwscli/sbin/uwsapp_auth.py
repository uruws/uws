#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

__doc__ = 'uwsapp users auth'

import json

from argparse import ArgumentParser
from os       import unlink
from uuid     import uuid5
from uuid     import NAMESPACE_DNS

import uwscli

from uwscli_auth import User
from uwscli_user import AppUser

def _apps_build(user: User) -> dict[str, str]:
	d = dict()
	for app in uwscli.build_list(user = user):
		d[app] = uwscli.app[app].desc
	return d

def _apps_deploy(user: User) -> dict[str, str]:
	d = dict()
	for app in uwscli.deploy_list(user = user):
		d[app] = uwscli.app[app].desc
	return d

def _json_dump(fn: str, data: dict[str, str]):
	with open(fn, 'w') as fh: # pragma: no cover
		json.dump(data, fh)

def _write_user(uid: str, data: dict[str, str]) -> int:
	fn = '/run/uwscli/auth/%s/meta.json' % uid
	newfn = '%s.new' % fn
	_json_dump(newfn, data)
	rc = uwscli.system('/usr/bin/install -v -m 0640 -u uws -g uws %s %s' % (newfn, fn))
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
		uid: str = str(uuid5(NAMESPACE_DNS, username))

		# user dir to save password
		rc = uwscli.system('/usr/bin/install -v -d -m 0750 -u uws -g uws /run/uwscli/auth/%s' % uid)
		if rc != 0: return rc

		# user info file
		u = User(user.name)
		d = {
			'uid': uid,
			'name': user.name,
			'username': username,
			'apps': {
				'build': _apps_build(u),
				'deploy': _apps_deploy(u),
			},
		}
		rc = _write_user(uid, d)
		if rc != 0: return rc

	return 0

if __name__ == '__main__': # pragma: no cover
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
