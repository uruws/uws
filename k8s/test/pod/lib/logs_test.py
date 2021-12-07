#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import logs

_bup_system = logs.system

_argv = ['-n', 'ns']

class Test(unittest.TestCase):

	def setUp(t):
		logs.system = MagicMock(return_value = 0)

	def tearDown(t):
		logs.system = None
		logs.system = _bup_system

	def test_main(t):
		t.assertEqual(logs.main(_argv), 0)
		logs.system.assert_called_once_with("uwskube logs --timestamps -n ns --tail=10 --prefix=true --ignore-errors -l '*'")

	def test_main_arg_errors(t):
		with t.assertRaises(SystemExit) as e:
			logs.main()
		err = e.exception
		t.assertEqual(err.args[0], 2)
		logs.system.assert_not_called()

	def test_main_follow(t):
		t.assertEqual(logs.main(['-n', 'ns', '-f']), 0)
		logs.system.assert_called_once_with("uwskube logs --timestamps -n ns --tail=10 -f --prefix=true --ignore-errors -l '*'")

if __name__ == '__main__':
	unittest.main()
