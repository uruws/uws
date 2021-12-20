#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import deploy

class Test(unittest.TestCase):

	def test_imports(t):
		t.assertEqual(deploy.deploy_generation.__name__, 'deploy_generation')
		t.assertEqual(deploy.deploy_condition.__name__, 'deploy_condition')
		t.assertEqual(deploy.deploy_status.__name__, 'deploy_status')

if __name__ == '__main__':
	unittest.main()
