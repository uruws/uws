# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pathlib  import Path

import uwscli

from uwscli_conf import CustomDeploy

class Config(object):
	fn:       str                = ''
	app_name: str                = ''
	app_env:  str                = ''
	deploy:   list[CustomDeploy] = []

	def __init__(c, fn: str, app_name: str, app_env: str):
		c.fn = Path(fn.strip()).stem
		c.app_name = app_name.strip()
		c.app_env = app_env.strip()

	def check(c):
		if c.fn == '':
			raise RuntimeError('custom_deploy.Config: empty fn')
		if c.app_name == '':
			raise RuntimeError('custom_deploy.Config: empty app_name')
		if c.app_env == '':
			raise RuntimeError('custom_deploy.Config: empty app_env')
		if not c.app_name in uwscli.deploy_list():
			raise RuntimeError(f"invalid app: {c.app_name}")
		c.deploy = uwscli.custom_deploy(c.app_name, c.app_env)
		if not c.deploy:
			raise RuntimeError(f"invalid app env: {c.app_name} {c.app_env}")
		return True

def main(argv: list[str], cfg: Config) -> int:
	epilog = f"{cfg.app_name} custom deploy for {cfg.app_env} environment"

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = epilog)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('version', metavar = 'X.Y.Z',
		default = '', help = 'deploy version')

	args = flags.parse_args(argv)

	try:
		cfg.check()
	except RuntimeError as err:
		uwscli.error(err)
		return 9

	uwscli.debug('custom deploy:', cfg.deploy)

	return 0
