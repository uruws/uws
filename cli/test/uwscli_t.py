# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock, call

from contextlib import contextmanager
from io import StringIO
from subprocess import getstatusoutput, check_output, CalledProcessError

import uwscli
import uwscli_conf

def _testingApp() -> dict[str, uwscli_conf.App]:
	return {
		'testing': uwscli_conf.App(True,
			cluster = 'ktest',
			desc = 'Testing',
			pod = 'test',
			build = uwscli_conf.AppBuild('/srv/deploy/Testing', 'build.sh', clean = 'testing'),
			deploy = uwscli_conf.AppDeploy('test'),
		),
	}

uwscli.app = _testingApp()

def _testingCluster() -> dict[str, uwscli_conf.AppCluster]:
	return {'ktest': uwscli_conf.AppCluster(region = 'testing-1')}

uwscli.cluster = _testingCluster()

uwscli.docker_storage = '/srv/docker'
uwscli.docker_storage_min = 10

def mock():
	uwscli._log = True
	uwscli._debug = False
	uwscli._outfh = None
	uwscli._outfh = StringIO()
	uwscli._errfh = None
	uwscli._errfh = StringIO()
	uwscli.app = None
	uwscli.app = _testingApp()
	uwscli.cluster = None
	uwscli.cluster = _testingCluster()

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
		uwscli._debug = False
		yield
	finally:
		uwscli._log = True
		uwscli._debug = False

@contextmanager
def mock_chdir(fail = False, faildir = ''):
	@contextmanager
	def __chdir(d, error_status = 2):
		try:
			if fail is True:
				raise SystemExit(error_status)
			if d == faildir:
				raise SystemExit(error_status)
			yield
		finally:
			pass
	chdir_bup = uwscli.chdir
	try:
		uwscli.chdir = MagicMock(side_effect = __chdir)
		yield
	finally:
		uwscli.chdir = chdir_bup

@contextmanager
def mock_mkdir(fail = False, fail_path = ''):
	def __mkdir(d, mode = 0o750, parents = True, exist_ok = True):
		if fail or fail_path == d:
			raise FileExistsError(d)
	mkdir_bup = uwscli.mkdir
	try:
		uwscli.mkdir = MagicMock(side_effect = __mkdir)
		yield
	finally:
		uwscli.mkdir = mkdir_bup

@contextmanager
def mock_system(status = 0, fail_cmd = '', fail_status = 99):
	def __system(cmd, env = None, timeout = 180):
		if fail_cmd and cmd.startswith(fail_cmd):
			return fail_status
		return status
	system_bup = uwscli.system
	try:
		uwscli.system = MagicMock(side_effect = __system)
		yield
	finally:
		uwscli.system = system_bup

@contextmanager
def mock_check_output(fail = False, output = 'mock_output'):
	def __co(*args, **kwargs):
		if fail:
			raise CalledProcessError(99, 'mock_cmd', output = output)
		return output
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

@contextmanager
def mock_list_images(return_value = []):
	li_bup = uwscli.list_images
	try:
		uwscli.list_images = MagicMock(return_value = return_value)
		yield
	finally:
		uwscli.list_images = li_bup

@contextmanager
def mock_git_deploy(status = 0):
	gd_bup = uwscli.git_deploy
	try:
		uwscli.git_deploy = MagicMock(return_value = status)
		yield
	finally:
		uwscli.git_deploy = gd_bup

@contextmanager
def mock_uwscli_deploy(status = 0):
	_bup = uwscli.uwscli_deploy
	try:
		uwscli.uwscli_deploy = MagicMock()
		uwscli.uwscli_deploy.run = MagicMock(return_value = status)
		yield
	finally:
		uwscli.uwscli_deploy = _bup
