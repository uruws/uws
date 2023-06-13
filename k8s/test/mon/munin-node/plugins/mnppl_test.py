#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from   unittest.mock import MagicMock, call

from pathlib import Path

import mon_t

import mnppl

_bup_print = mnppl._print

testing_plugins_bindir = './k8s/test/mon/munin-node/plugins/mnppl'

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		mnppl._print = MagicMock()

	def test_globals(t):
		t.assertEqual(mnppl.plugins_bindir, '/usr/local/bin')
		t.assertEqual(mnppl.plugins_suffix, '.mnppl')
		t.assertEqual(mnppl.time_warning,   270)
		t.assertEqual(mnppl.time_critical,  290)
		t.assertEqual(mnppl.plwait_timeout, 240)

	#
	# configs and reports
	#

	def test_print(t):
		_bup_print('testing', '...')

	def test_config(t):
		mnppl._config()
		config = [
			call('multigraph mnppl'),
			call('graph_title k8stest mnppl'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category munin'),
			call('graph_vlabel seconds'),
			call('graph_printf %3.3lf'),
			call('graph_scale yes'),
			call('mnppl.label total'),
			call('mnppl.colour COLOUR0'),
			call('mnppl.draw AREA'),
			call('mnppl.min 0'),
			call('mnppl.warning', mnppl.time_warning),
			call('mnppl.critical', mnppl.time_critical),
		]
		mnppl._print.assert_has_calls(config)
		t.assertEqual(mnppl._print.call_count, len(config))

	def test_report(t):
		mnppl._report(0.3)
		report = [
			call('multigraph mnppl'),
			call('mnppl.value', 0.3),
		]
		mnppl._print.assert_has_calls(report)
		t.assertEqual(mnppl._print.call_count, len(report))

	#
	# run parallel
	#

	def test_listPlugins(t):
		t.assertListEqual(mnppl._listPlugins(testing_plugins_bindir), [
			't0.mnppl',
			't1.mnppl',
			't2.mnppl',
			't3.mnppl',
			't4.mnppl',
		])

	def test_run_config(t):
		d = Path(testing_plugins_bindir, 'run')
		t.assertEqual(mnppl._run(d, 'config'), 0)

	def test_run_report(t):
		d = Path(testing_plugins_bindir, 'run')
		t.assertEqual(mnppl._run(d, 'report'), 0)

	def test_run_fail(t):
		d = Path(testing_plugins_bindir, 'fail')
		t.assertEqual(mnppl._run(d, 'report'), 128)

	#
	# main
	#

	def test_main_config(t):
		d = Path(testing_plugins_bindir, 'run').as_posix()
		t.assertEqual(mnppl.main(['-b', d, 'config']), 0)

	def test_main_no_plugins(t):
		t.assertEqual(mnppl.main([]), 0)

if __name__ == '__main__':
	unittest.main()
