#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t

import admin_cluster

class TestCluster(unittest.TestCase):

	#---------------------------------------------------------------------------
	# /cluster/

	def test_index(t):
		with admin_t.mock() as m:
			admin_cluster.index('k8stest')
			t.assertEqual(m.response.status, 200)
			m.template.assert_called_once_with('admin/cluster_index.html',
				admin_cluster = 'k8stest', has_error = False)

	def test_index_error(t):
		with admin_t.mock() as m:
			admin_cluster.index('no-cluster')
			m.error.assert_called_once_with(404, 'admin/cluster_index.html',
				admin_cluster = 'no-cluster', has_error = True)

if __name__ == '__main__':
	unittest.main()
