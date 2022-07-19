#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

__doc__ = 'setup uwscli environment'

from argparse import ArgumentParser

import uwscli
import uwscli_conf as conf

class _cmdFailed(Exception):
	rc = -1

	def __init__(self, rc):
		super().__init__()
		self.rc = rc

def _run(cmd, args: list[str] = []):
	uwscli.debug('***', cmd)
	x = f"{conf.sbindir}/{cmd}"
	if len(args) > 0:
		x = f"{x} {' '.join(args)}"
	uwscli.log('***', x)
	rc = uwscli.system(x, env = {'PATH': '/bin:/usr/bin:/sbin:/usr/sbin'})
	if rc != 0:
		uwscli.error(f"{cmd}: exit status {rc}")
		raise _cmdFailed(rc)

def main(argv: list[str] = []) -> int:
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	args = flags.parse_args(argv)

	try:
		# filesystem, users and groups setup
		_run('uwscli_setup.sh')

		# app groups
		_run('uwscli_app.sh', uwscli.app_groups())

		# user
		user_list = uwscli.user_list()
		user_remove = []
		admin_list = []
		operator_list = []

		for user in user_list:
			# remove
			if user.remove:
				user_remove.append(user.name)
				continue
			# admins
			if user.is_admin:
				admin_list.append(user.name)
			# operators
			if user.is_operator:
				operator_list.append(user.name)
			# setup
			_run('uwscli_user.sh', [conf.homedir, str(user.uid), user.name])
			# groups
			args = [user.name]
			args.extend(user.groups)
			_run('uwscli_user_groups.sh', args)
			# authkeys
			if user.keyid != '':
				_run('uwscli_user_authkeys.sh', [conf.homedir, user.name, user.keyid])

		# admin
		if len(admin_list) > 0:
			_run('uwscli_admin.sh', admin_list)

		# operator
		if len(operator_list) > 0:
			_run('uwscli_operator.sh', operator_list)

		# uwsapp users auth
		_run('uwsapp_auth.py')

		# user remove
		for name in user_remove:
			_run('uwscli_user_remove.sh', [name])

		# buildpack
		_run('buildpack_setup.sh', ['/srv/deploy/Buildpack', uwscli.buildpack_repo()])
		for app in uwscli.build_repo():
			uwscli.log('app repo:', app['app'])
			_run('app_repo.sh', [app['uri'], app['workdir']])

	except _cmdFailed as err:
		return err.rc

	return 0

if __name__ == '__main__': # pragma: no cover
	sys.stdout.reconfigure(line_buffering = False)
	sys.stderr.reconfigure(line_buffering = False)
	sys.exit(main(sys.argv[1:]))
