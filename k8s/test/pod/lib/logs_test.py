#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import logs

_bup_system = logs._system

_argv = ['-n', 'ns']

class Test(unittest.TestCase):

	def setUp(t):
		logs._system = MagicMock(return_value = 0)

	def tearDown(t):
		logs._system = None
		logs._system = _bup_system

	def test_system(t):
		t.assertEqual(_bup_system('exit 0'), 0)

	def test_main(t):
		t.assertEqual(logs.main(_argv), 0)
		logs._system.assert_called_once_with("uwskube logs --timestamps -n ns --tail=10 --prefix=true --ignore-errors -l '*'")

	def test_main_arg_errors(t):
		with t.assertRaises(SystemExit) as e:
			logs.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)
		logs._system.assert_not_called()

	def test_main_follow(t):
		t.assertEqual(logs.main(['-n', 'ns', '-f']), 0)
		logs._system.assert_called_once_with("uwskube logs --timestamps -n ns --tail=10 -f --prefix=true --ignore-errors -l '*'")

	def test_main_pod(t):
		t.assertEqual(logs.main(['-n', 'ns', 'pod/testing']), 0)
		logs._system.assert_called_once_with("uwskube logs --timestamps -n ns --tail=10 pod/testing")

	def test_main_pod_error(t):
		logs._system = MagicMock(return_value = 99)
		t.assertEqual(logs.main(['-n', 'ns', 'pod/testing']), 99)

if __name__ == '__main__':
	unittest.main()
