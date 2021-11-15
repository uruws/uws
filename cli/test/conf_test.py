#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import uwscli_conf

class Test(unittest.TestCase):

	def test_defaults(t):
		t.assertEqual(uwscli_conf.bindir, '/srv/home/uwscli/bin')
		t.assertEqual(uwscli_conf.cmddir, '/srv/uws/deploy/cli')
		t.assertEqual(uwscli_conf.deploy_testdir, '/srv/test')
		t.assertEqual(uwscli_conf.docker_storage, '/srv/docker/lib')
		t.assertEqual(uwscli_conf.docker_storage_min, 10485760)
		t.assertIsInstance(uwscli_conf.app, dict)
		t.assertIsInstance(uwscli_conf.cluster, dict)

if __name__ == '__main__':
	unittest.main()
