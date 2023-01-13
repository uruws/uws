#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from   unittest.mock import MagicMock

import sys
sys.path.insert(0, '/srv/uws/deploy/secret/cli/schroot/prod')

import uwscli
import uwscli_auth
import uwscli_conf
import uwscli_user
import local_conf # type: ignore

class Test(unittest.TestCase):

	@classmethod
	def setUpClass(c):
		uwscli_auth.getstatusoutput = MagicMock(return_value = (0, uwscli_conf.admin_group))

	def test_defaults(t):
		t.assertEqual(uwscli.docker_storage,     '/var/lib/docker')
		t.assertEqual(uwscli.docker_storage_min, 10*1024*1024)

	def test_prod_users(t):
		# users
		t.assertListEqual([u.name for u in uwscli.user_list()], [
			'jeremias',
		])

if __name__ == '__main__':
	unittest.main()
