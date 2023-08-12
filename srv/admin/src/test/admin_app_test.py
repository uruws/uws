#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import admin_t

import admin_app

class TestCluster(unittest.TestCase):

	#---------------------------------------------------------------------------
	# /app/

	def test_index(t):
		with admin_t.mock() as m:
			admin_app.index('apptest')
			m.template.assert_called_once_with('admin/app_index.html', admin_app = 'apptest')

	def test_index_error(t):
		with admin_t.mock() as m:
			admin_app.index('')
			m.error.assert_called_once_with(404, 'admin/app_index.html', admin_app = '')

if __name__ == '__main__':
	unittest.main()
