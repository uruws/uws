#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t

import admintpl

class TestAdminTpl(unittest.TestCase):

	def test_exports(t):
		t.assertListEqual(sorted([s for s in dir(admintpl) if not s.startswith('_')]), [
			'admin',
			'button_class',
			'button_color',
			'button_current',
			'cluster_sidebar',
			'input_class',
			'input_color',
			'url',
			'wapp',
		])

	#---------------------------------------------------------------------------
	# cluster

	def test_cluster_sidebar(t):
		with admin_t.mock() as m:
			t.assertDictEqual(admintpl.cluster_sidebar(), {
				'k8stest': '/cluster/k8stest/',
			})

if __name__ == '__main__':
	unittest.main()
