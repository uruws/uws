#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

from email.headerregistry import Address

import alerts

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(alerts.QDIR, '/var/opt/munin-alert')
		t.assertEqual(alerts.MAILTO,
			Address('munin alert', 'munin-alert', 'uws.talkingpts.org'))

if __name__ == '__main__':
	unittest.main()
