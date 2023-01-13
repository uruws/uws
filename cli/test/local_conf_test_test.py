#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from   unittest.mock import MagicMock

import sys
sys.path.insert(0, '/srv/uws/deploy/secret/cli/schroot/test')

import uwscli
import uwscli_auth
import uwscli_conf
import uwscli_user
import local_conf # type: ignore

class Test(unittest.TestCase):

	@classmethod
	def setUpClass(c):
		uwscli_auth.getstatusoutput = MagicMock(return_value = (0, uwscli_conf.admin_group))

	def test_defaults(t):
		t.assertEqual(uwscli.bindir,             '/srv/home/uwscli/bin')
		t.assertEqual(uwscli.cmddir,             '/srv/uws/deploy/cli')
		t.assertEqual(uwscli.docker_storage,     '/var/lib/docker')
		t.assertEqual(uwscli.docker_storage_min, 5*1024*1024)

	def test_test_settings(t):
		# users
		t.assertListEqual([u.name for u in uwscli.user_list()], [
			'jeremias',
			'mauro',
			'santiago',
		])
		# cluster
		t.assertListEqual(sorted(uwscli.cluster.keys()), [
			'apptest-west',
			'panoramix-2206',
		])
		# app list
		app_list = [
			'infra-ui-prod',
			'infra-ui-test',
			'podtest',
		]
		# deploy
		t.assertListEqual(uwscli.deploy_list(), app_list)
		# app
		t.assertListEqual(uwscli.app_list(), app_list)
		# build
		t.assertListEqual(uwscli.build_list(), [
			'infra-ui',
			'uwspod',
		])
		# autobuild
		t.assertListEqual(uwscli.autobuild_list(), [
			'infra-ui',
			'uwspod',
		])

if __name__ == '__main__':
	unittest.main()
