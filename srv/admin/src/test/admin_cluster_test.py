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
			admin_cluster.index()
			m.template.assert_called_once_with('admin/cluster_index.html', cluster = '')

if __name__ == '__main__':
	unittest.main()
