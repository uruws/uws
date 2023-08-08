#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import munin

class Test(unittest.TestCase):

	def setUp(k):
		munin.mnpl.config_host = MagicMock(return_value = 0)
		munin.mnpl.report_host = MagicMock(return_value = 0)
		munin.mon.cluster = MagicMock(return_value = 'k8stest')

	def test_host(t):
		h = munin._host()
		t.assertEqual(h.name, 'ops')
		t.assertEqual(h.host, 'ops')

	def test_cfg(t):
		cfg = munin._cfg()
		t.assertEqual(cfg.path,
			'/munin/uws.t.o/cluster.uws.t.o/k8s_k8stest__k8smon___ping_400_no_auth-day.png')
		t.assertEqual(cfg.category, 'munin')
		t.assertEqual(cfg.title, 'munin crosscheck')

	def test_config(t):
		t.assertEqual(munin.main(['config']), 0)
		munin.mnpl.report_host.assert_not_called()
		munin.mnpl.config_host.assert_called_once()

	def test_report(t):
		t.assertEqual(munin.main([]), 0)
		munin.mnpl.config_host.assert_not_called()
		munin.mnpl.report_host.assert_called_once()

if __name__ == '__main__':
	unittest.main()
