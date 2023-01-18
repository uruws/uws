# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import uwscli

from uwscli_conf import CustomDeploy

class Config(object):
	app_name: str                = ''
	app_env:  str                = ''
	deploy:   list[CustomDeploy] = []

	def __init__(c, app_name: str, app_env: str):
		c.app_name = app_name.strip()
		c.app_env = app_env.strip()

	def check(c):
		if c.app_name == '':
			raise RuntimeError('custom_deploy.Config: empty app_name')
		if c.app_env == '':
			raise RuntimeError('custom_deploy.Config: empty app_env')
		if not c.app_name in uwscli.build_list():
			raise RuntimeError(f"invalid app: {c.app_name}")
		c.deploy = uwscli.custom_deploy(c.app_name, c.app_env)
		if not c.deploy:
			raise RuntimeError(f"invalid app env: {c.app_name} {c.app_env}")
		return True

def rollback(app: str) -> int:
	uwscli.debug('rollback:', app)
	args = "%s %s rollback" % (uwscli.app[app].cluster,
		uwscli.app[app].pod)
	return uwscli.ctl(args)

def _do_rollback(l: list[CustomDeploy]):
	for d in l:
		uwscli.log('*** app-rollback', d.app)
		rollback(d.app)

def show_builds(app: str) -> int:
	images = uwscli.list_images(app)
	if len(images) > 0:
		uwscli.log('available', app, 'builds:')
		for n in images:
			uwscli.log(' ', n)
	else:
		uwscli.log('no builds available for', app)
	return 3

def deploy(version: str, cfg: Config) -> int:
	if version == '':
		n = cfg.deploy[0].app
		return show_builds(n)

	# rollback list
	rbl: list[CustomDeploy] = []

	uwscli.debug('custom deploy:', cfg.deploy)
	for d in cfg.deploy:
		uwscli.log('*** app-deploy', d.app)
		cmd = f"{uwscli.bindir}/app-deploy --wait --rollback {d.app} {version}"
		rc = uwscli.system(cmd)
		if rc != 0:
			_do_rollback(rbl)
			return rc
		rbl.append(d)

	return 0

def action_run(name: str, cfg: Config) -> int:
	for d in cfg.deploy:
		uwscli.log(f"*** app-{name}", d.app)
		cmd = f"{uwscli.bindir}/app-{name} {d.app}"
		uwscli.system(cmd)
	return 0

def main(argv: list[str], cfg: Config) -> int:
	epilog = f"{cfg.app_name} custom deploy for {cfg.app_env} environment"

	commands = ['deploy', 'status']
	action = 'command'

	if 'deploy' in argv:
		action = 'deploy'
		epilog += '\nif no deploy version is provided show list of available builds'
	else:
		epilog += '\n\navailable command:\n'
		for c in commands:
			epilog += f"  {c}\n"

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = epilog)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('action', metavar = action, default = 'status',
		help = 'command action', choices = commands.copy())

	if action == 'deploy':
		flags.add_argument('version', metavar = 'X.Y.Z', nargs = '?',
			default = '', help = 'deploy version')

	args = flags.parse_args(argv)

	try:
		cfg.check()
	except RuntimeError as err:
		uwscli.error(err)
		return 10

	if args.action == 'deploy':
		return deploy(args.version, cfg)
	else:
		if args.action in commands:
			return action_run(args.action.strip(), cfg)

	uwscli.error('[ERROR] invalid action:', args.action)
	return 9
