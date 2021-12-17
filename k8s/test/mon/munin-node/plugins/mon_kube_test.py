#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
# ~ from unittest.mock import MagicMock, call

import mon_kube

class Test(unittest.TestCase):

	def test_globals(t):
		t.assertEqual(mon_kube._uwskube_url,
			'http://k8s.mon.svc.cluster.local:2800/kube')
		t.assertEqual(mon_kube.UWSKUBE_URL, mon_kube._uwskube_url)

	def test_main(t):
		pass

if __name__ == '__main__':
	unittest.main()
