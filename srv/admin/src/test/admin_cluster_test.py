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
			m.template.assert_called_once_with('admin/cluster_index.html', admin_cluster = 'k8stest', has_error = False)

if __name__ == '__main__':
	unittest.main()
