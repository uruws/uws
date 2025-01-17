#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import uwscli
import uwscli_conf
import uwscli_auth

from uwscli_conf import CustomDeploy

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
			'appc5nxl-2309',
			'apptest-2302',
			'pnt-2308',
			'wrkrc5nxl-2309',
		])
		# app list
		app_list = [
			'api-prod',
			'api-test',
			'app-prod',
			'app-test',
			'appcdn-prod',
			'appcdn-test',
			'cs',
			'cs-test',
			'meteor-vanilla',
			'sarmiento-hpx',
			'sarmiento-ngx',
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
			'meteor-vanilla',
		])
		# autobuild
		t.assertListEqual(uwscli.autobuild_list(), [
			'app',
			'cs',
			'meteor-vanilla',
		])

	def test_app_build_group(t):
		for appname, app in uwscli_conf.app.items():
			if app.build.dir != '':
				group_ok = False
				for g in app.groups:
					if g == "uwsapp_%s" % appname:
						group_ok = True
				t.assertTrue(group_ok, appname)

	def test_custom_deploy(t):
		t.assertDictEqual(uwscli.app['app'].custom_deploy, {
			'production': [
				CustomDeploy('worker'),
				CustomDeploy('api-prod'),
				CustomDeploy('app-prod'),
			],
			'staging': [
				CustomDeploy('worker-test'),
				CustomDeploy('api-test'),
				CustomDeploy('app-test'),
			],
		})

if __name__ == '__main__':
	unittest.main()
