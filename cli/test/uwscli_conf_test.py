#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli
import uwscli_conf

class Test(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(uwscli_conf.bindir, '/srv/home/uwscli/bin')
		t.assertEqual(uwscli_conf.cmddir, '/srv/uws/deploy/cli')
		t.assertEqual(uwscli_conf.deploy_basedir, '/srv/deploy')
		t.assertEqual(uwscli_conf.docker_storage, '/srv/docker/lib')
		t.assertEqual(uwscli_conf.docker_storage_min, 10485760)
		t.assertIsInstance(uwscli_conf.app, dict)
		t.assertIsInstance(uwscli_conf.cluster, dict)

	def test_prod_settings(t):
		app_list = [
			'app-east',
			'app-west',
			'beta',
			'cs',
			'nlp-sentiment-roberta',
			'nlp-topic-automl',
			'worker',
		]
		# deploy list
		t.assertListEqual(uwscli.deploy_list(), app_list)
		# app list
		t.assertListEqual(uwscli.app_list(), app_list)
		# build list
		t.assertListEqual(uwscli.build_list(), [
			'app',
			'beta',
			'cs',
			'nlpsvc',
		])

if __name__ == '__main__':
	unittest.main()
