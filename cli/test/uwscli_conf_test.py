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
		# cluster
		t.assertListEqual(sorted(uwscli.cluster.keys()), [
			'amy-east',
			'amy-test-1',
			'amy-test-2',
			'amy-west',
			'amy-wrkr',
			'amybeta',
			'panoramix',
		])
		# app list
		app_list = [
			'app-east',
			'app-test-1',
			'app-test-2',
			'app-west',
			'beta',
			'cs',
			'nlp-category',
			'nlp-sentiment-roberta',
			'nlp-topic-automl',
			'worker',
		]
		# deploy
		t.assertListEqual(uwscli.deploy_list(), app_list)
		# app
		t.assertListEqual(uwscli.app_list(), app_list)
		# build
		t.assertListEqual(uwscli.build_list(), [
			'app',
			'beta',
			'cs',
			'nlpsvc',
		])
		# autobuild
		t.assertListEqual(uwscli.autobuild_list(), [
			'app',
		])

if __name__ == '__main__':
	unittest.main()
