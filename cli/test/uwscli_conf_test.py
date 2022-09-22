#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import uwscli
import uwscli_conf
import uwscli_auth

class Test(unittest.TestCase):

	@classmethod
	def setUpClass(c):
		uwscli_auth.getstatusoutput = MagicMock(return_value = (0, uwscli_conf.admin_group))

	def test_defaults(t):
		t.assertEqual(uwscli_conf.homedir, '/home')
		t.assertEqual(uwscli_conf.sbindir, '/srv/home/uwscli/sbin')
		t.assertEqual(uwscli_conf.bindir, '/srv/home/uwscli/bin')
		t.assertEqual(uwscli_conf.cmddir, '/srv/uws/deploy/cli')
		t.assertEqual(uwscli_conf.deploy_basedir, '/srv/deploy')
		t.assertEqual(uwscli_conf.docker_storage, '/srv/docker')
		t.assertEqual(uwscli_conf.docker_storage_min, 10485760)
		t.assertIsInstance(uwscli_conf.app, dict)
		t.assertIsInstance(uwscli_conf.cluster, dict)

	def test_prod_settings(t):
		# cluster
		t.assertListEqual(sorted(uwscli.cluster.keys()), [
			'app-east',
			'app-east-2209',
			'app-west',
			'apptest-east',
			'apptest-west',
			'panoramix-2206',
			'worker-2209',
		])
		# app list
		app_list = [
			'app-east',
			'app-west',
			'apptest-east',
			'apptest-west',
			'cs',
			'cs-test',
			'infra-ui-prod',
			'infra-ui-test',
			'nlp-category',
			'nlp-sentiment-twitter',
			'worker',
			'worker-test',
		]
		# deploy
		t.assertListEqual(uwscli.deploy_list(), app_list)
		# app
		t.assertListEqual(uwscli.app_list(), app_list)
		# build
		t.assertListEqual(uwscli.build_list(), [
			'app',
			'cs',
			'infra-ui',
			'nlpsvc',
		])
		# autobuild
		t.assertListEqual(uwscli.autobuild_list(), [
			'app',
			'cs',
			'infra-ui',
		])

	def test_app_build_group(t):
		for appname, app in uwscli_conf.app.items():
			if app.build.dir != '':
				group_ok = False
				for g in app.groups:
					if g == "uwsapp_%s" % appname:
						group_ok = True
				t.assertTrue(group_ok, appname)

if __name__ == '__main__':
	unittest.main()
