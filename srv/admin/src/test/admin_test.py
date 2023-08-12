#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t
import admin_test_conf

import uwscli_conf # type: ignore

import admin

cluster_k8stest = admin.Cluster(name = 'k8stest', region = 'uy-test-0')
apptest = admin.App(name = 'apptest', cluster = 'k8stest')

class TestAdmin(unittest.TestCase):

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

if __name__ == '__main__':
	unittest.main()
