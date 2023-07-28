#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import abtpl

class TestABTpl(unittest.TestCase):

	def test_settings(t):
		t.assertListEqual(sorted([s for s in dir(abtpl) if not s.startswith('_')]), [
			'button_class',
			'button_color',
			'button_current',
			'input_class',
			'input_color',
		])

if __name__ == '__main__':
	unittest.main()
