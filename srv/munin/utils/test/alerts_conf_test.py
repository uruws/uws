#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import unittest

from email.headerregistry import Address

from pathlib import Path

from time import localtime
from time import tzset

import alerts_conf as conf

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(conf.QDIR, '/var/opt/munin-alert')
		t.assertEqual(conf.DOMAIN, 'uws.talkingpts.org')

		t.assertEqual(conf.MAILTO,
			Address('munin alert', 'munin-alert', 'uws.talkingpts.org'))
		t.assertEqual(conf.MAILTO_REPORT,
			Address('munin report', 'munin-report', 'uws.talkingpts.org'))

		t.assertEqual(conf.SLEEP_TZ, 'UTC')

	def test_sleepingHours(t):
		conf.sleepingHours()
		check = dict()
		for h in range(0, 25):
			check[h] = conf.sleepingHours(h)
		t.assertDictEqual(check, {
			0: False,
			1: True,
			2: True,
			3: True,
			4: True,
			5: True,
			6: True,
			7: True,
			8: True,
			9: True,
			10: False,
			11: False,
			12: False,
			13: False,
			14: False,
			15: False,
			16: False,
			17: False,
			18: False,
			19: False,
			20: False,
			21: False,
			22: False,
			23: False,
			24: False,
		})

	def test_sleepTZ(t):
		try:
			conf.SLEEP_TZ = 'America/Montevideo'
			conf._gethour()
			h = localtime()
			t.assertEqual(h.tm_zone, '-03')
			t.assertEqual(h.tm_gmtoff, -10800)
		finally:
			conf.SLEEP_TZ = 'UTC'
			os.environ['TZ'] = 'UTC'
			tzset()

if __name__ == '__main__':
	unittest.main()
