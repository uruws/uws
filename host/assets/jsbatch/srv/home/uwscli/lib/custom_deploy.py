# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pathlib  import Path

class Config(object):
	fn:       str = ''
	app_name: str = ''
	app_env:  str = ''

	def __init__(c, fn: str, app_name: str, app_env: str):
		c.fn = Path(fn.strip()).stem
		c.app_name = app_name
		c.app_env = app_env

	def check(c):
		if c.fn == '':
			raise RuntimeError('custom_deploy.Config: empty fn')
		if c.app_name == '':
			raise RuntimeError('custom_deploy.Config: empty app_name')
		if c.app_env == '':
			raise RuntimeError('custom_deploy.Config: empty app_env')

def main(cfg: Config) -> int:
	cfg.check()

	epilog = f"{cfg.app_name} custom deploy for {cfg.app_env} environment"

	flags = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
		description = __doc__, epilog = epilog)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())

	args = flags.parse_args(argv)

	return 0
