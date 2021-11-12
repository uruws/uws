# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from contextlib import contextmanager
from io import StringIO
from subprocess import getstatusoutput, check_output, CalledProcessError

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

uwscli.docker_storage = '/srv/docker'
uwscli.docker_storage_min = 10

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

@contextmanager
def mock_check_output(fail = False):
	def __co(*args, **kwargs):
		if fail:
			raise CalledProcessError(99, 'mock_cmd', output = 'mock_output')
		return b'mock_output'
	co_bup = uwscli.check_output
	try:
		uwscli.check_output = MagicMock(side_effect = __co)
		yield
	finally:
		uwscli.check_output = co_bup

@contextmanager
def mock_gso(status = 0, output = 'mock_output'):
	gso_bup = uwscli.gso
	try:
		uwscli.gso = MagicMock(return_value = (status, output))
		yield
	finally:
		uwscli.gso = gso_bup
