#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t
import admin_test

import admintpl

class TestAdminTpl(unittest.TestCase):

	def test_exports(t):
		t.assertListEqual(sorted([s for s in dir(admintpl) if not s.startswith('_')]), [
			'admin',
			'button_class',
			'button_color',
			'button_current',
			'cluster_info',
			'cluster_navbar',
			'input_class',
			'input_color',
			'log',
			'url',
			'wapp',
		])

	#---------------------------------------------------------------------------
	# cluster

	def test_cluster_navbar(t):
		with admin_t.mock() as m:
			t.assertDictEqual(admintpl.cluster_navbar(), {
				'k8stest': '/cluster/k8stest/',
			})

	def test_cluster_info(t):
		with admin_t.mock() as m:
			t.assertEqual(admintpl.cluster_info('k8stest'), admin_test.cluster_k8stest)

	def test_cluster_info_error(t):
		with admin_t.mock() as m:
			t.assertIsNone(admintpl.cluster_info(''))

if __name__ == '__main__':
	unittest.main()
