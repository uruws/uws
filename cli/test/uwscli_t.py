# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

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
	'testing1': uwscli_conf.App(True,
		cluster = 'ktest1',
		desc = 'Testing1',
		pod = 'test1',
		build = uwscli_conf.AppBuild('/srv/deploy/Testing1', 'build.sh'),
		deploy = uwscli_conf.AppDeploy('test1'),
	),
}

uwscli.cluster = {
	'ktest': {
		'region': 'testing-1',
	},
	'ktest1': {
		'region': 'testing-2',
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
