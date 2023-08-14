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
			'app_info',
			'app_list',
			'button_class',
			'button_color',
			'button_current',
			'cluster_info',
			'cluster_list',
			'config',
			'input_class',
			'input_color',
			'log',
			're',
			'slug',
			'url',
			'wapp',
		])

	#---------------------------------------------------------------------------
	# utils

	def test_slug(t):
		t.assertEqual(admintpl.slug('_te-st ing '), '_te_st_ing_')

	#---------------------------------------------------------------------------
	# cluster

	def test_cluster_list(t):
		with admin_t.mock() as m:
			t.assertListEqual(admintpl.cluster_list(), [admin_test.cluster_k8stest])

	def test_cluster_info(t):
		with admin_t.mock() as m:
			t.assertEqual(admintpl.cluster_info('k8stest'), admin_test.cluster_k8stest)

	def test_cluster_info_error(t):
		with admin_t.mock() as m:
			t.assertIsNone(admintpl.cluster_info(''))

	#---------------------------------------------------------------------------
	# app

	def test_app_list(t):
		with admin_t.mock() as m:
			t.assertListEqual(admintpl.app_list(), [admin_test.apptest])

	def test_app_info(t):
		with admin_t.mock() as m:
			t.assertEqual(admintpl.app_info('apptest'), admin_test.apptest)

	def test_app_info_error(t):
		with admin_t.mock() as m:
			t.assertIsNone(admintpl.app_info(''))

if __name__ == '__main__':
	unittest.main()
