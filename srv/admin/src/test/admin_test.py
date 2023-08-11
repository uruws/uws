#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t
import admin_test_conf

import admin

cluster_k8stest = admin.Cluster(name = 'k8stest', region = 'uy-test-0')

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

if __name__ == '__main__':
	unittest.main()
