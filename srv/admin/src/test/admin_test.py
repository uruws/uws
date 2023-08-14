#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t
import admin_test_conf

import uwscli_conf # type: ignore

import admin

cluster_k8stest = admin.Cluster(name = 'k8stest', region = 'uy-test-0')
apptest = admin.App(name = 'apptest', cluster = 'k8stest', region = 'uy-test-0')

class TestAdmin(unittest.TestCase):

	#---------------------------------------------------------------------------
	# config

	def test_config(t):
		with admin_t.mock() as m:
			t.assertEqual(admin.config.domain, 'testing.uws.local')

	#---------------------------------------------------------------------------
	# cluster

	def test_cluster_list(t):
		with admin_t.mock() as m:
			t.assertListEqual(admin.cluster_list(), [cluster_k8stest])

	def test_cluster_info(t):
		with admin_t.mock() as m:
			t.assertEqual(admin.cluster_info('k8stest'), cluster_k8stest)

	def test_cluster_info_error(t):
		with admin_t.mock() as m:
			with t.assertRaises(admin.ClusterError) as err:
				admin.cluster_info('')
			t.assertEqual(str(err.exception), '[empty]: cluster not found')

	#---------------------------------------------------------------------------
	# app

	def test_app_new(t):
		with admin_t.mock() as m:
			t.assertEqual(admin.app_info('apptest'), apptest)

	def test_app_list(t):
		with admin_t.mock() as m:
			t.assertListEqual(admin.app_list(), [apptest])

	def test_app_info(t):
		with admin_t.mock() as m:
			t.assertEqual(admin.app_info('apptest'), apptest)

	def test_app_info_error(t):
		with admin_t.mock() as m:
			with t.assertRaises(admin.AppError) as err:
				admin.app_info('')
			t.assertEqual(str(err.exception), '[empty]: app not found')

	def test_app_pod_containers(t):
		with admin_t.mock() as m:
			admin_test_conf.apptest.pod_containers = ['testing/pod', 'testing/pod1']
			a = admin.app_info('apptest')
			t.assertListEqual(a.pod_containers(), ['testing/pod', 'testing/pod1'])

if __name__ == '__main__':
	unittest.main()
