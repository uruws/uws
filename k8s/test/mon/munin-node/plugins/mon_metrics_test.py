#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import re
import unittest

import mon_t
import mon_metrics

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()

	def tearDown(t):
		mon_t.tearDown()

	def test_regexs(t):
		t.assertIsInstance(mon_metrics.parse_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line1_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line2_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line3_re, re.Pattern)
		t.assertIsInstance(mon_metrics.line4_re, re.Pattern)

if __name__ == '__main__':
	unittest.main()
