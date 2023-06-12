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

stats = {
	't0.mnppl': 0.1,
	't1.mnppl': 0.2,
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		mnppl._print = MagicMock()

	def test_globals(t):
		t.assertEqual(mnppl.plugins_bindir, '/usr/local/bin')
		t.assertEqual(mnppl.plugins_suffix, '.mnppl')
		t.assertEqual(mnppl.pool_wait,      300)
		t.assertEqual(mnppl.time_warning,   270)
		t.assertEqual(mnppl.time_critical,  290)

	#
	# configs and reports
	#

	def test_print(t):
		_bup_print('testing', '...')

	def test_config(t):
		mnppl._config(stats)
		config = [
			call('multigraph mnppl'),
			call('graph_title k8stest mnppl'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category munin'),
			call('graph_vlabel seconds'),
			call('graph_printf %3.3lf'),
			call('graph_scale yes'),
			call('total_mnppl.label total'),
			call('total_mnppl.colour COLOUR0'),
			call('total_mnppl.draw LINE'),
			call('total_mnppl.min 0'),
			call('total_mnppl.max 400'),
			call('total_mnppl.warning', 270),
			call('total_mnppl.critical', 290),
			call('t0_mnppl.label', 't0'),
			call('t0_mnppl.colour COLOUR1'),
			call('t0_mnppl.draw AREA'),
			call('t0_mnppl.min 0'),
			call('t0_mnppl.max 400'),
			call('t1_mnppl.label', 't1'),
			call('t1_mnppl.colour COLOUR2'),
			call('t1_mnppl.draw AREA'),
			call('t1_mnppl.min 0'),
			call('t1_mnppl.max 400'),
		]
		mnppl._print.assert_has_calls(config)
		t.assertEqual(mnppl._print.call_count, len(config))

	def test_report(t):
		stats['total.mnppl'] = 0.3
		mnppl._report(stats)
		report = [
			call('multigraph mnppl'),
			call('t0_mnppl.value', 0.1),
			call('t1_mnppl.value', 0.2),
			call('total_mnppl.value', 0.3),
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

	#
	# main
	#

	def test_main_config(t):
		d = Path(testing_plugins_bindir, 'run').as_posix()
		t.assertEqual(mnppl.main(['-b', d, 'config']), 0)

	def test_main_no_plugins(t):
		t.assertEqual(mnppl.main([]), 1)

	def test_main_no_parallel(t):
		t.assertEqual(mnppl.main(['--serial']), 0)

if __name__ == '__main__':
	unittest.main()
