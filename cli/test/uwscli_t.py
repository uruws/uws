# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from contextlib import contextmanager
from io import StringIO

import uwscli
import uwscli_conf

uwscli.app = {
	'testing': uwscli_conf.App(True,
		cluster = 'ktest',
		desc = 'Testing',
		pod = 'test',
		build = uwscli_conf.AppBuild('/srv/deploy/Testing', 'build.sh'),
		deploy = uwscli_conf.AppDeploy('test'),
	),
}

uwscli.cluster = {
	'ktest': {
		'region': 'testing-1',
	},
}

def mock():
	uwscli._outfh = None
	uwscli._outfh = StringIO()
	uwscli._errfh = None
	uwscli._errfh = StringIO()

def out():
	uwscli._outfh.seek(0, 0)
	s = uwscli._outfh.read()
	uwscli._outfh.seek(0, 0)
	uwscli._outfh.truncate()
	return s

def err():
	uwscli._errfh.seek(0, 0)
	s = uwscli._errfh.read()
	uwscli._errfh.seek(0, 0)
	uwscli._errfh.truncate()
	return s


@contextmanager
def log_disable():
	try:
		uwscli._log = False
		yield
	finally:
		uwscli._log = True

@contextmanager
def mock_system(status = 0):
	system_bup = uwscli.system
	try:
		uwscli.system = MagicMock(return_value = status)
		yield
	finally:
		uwscli.system = system_bup
