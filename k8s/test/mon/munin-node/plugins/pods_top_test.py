#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import pods_top

_bup_print = pods_top._print

_pods = {
	'items': [
		{
			'namespace': 'cert-manager',
			'name': 'cert-manager-66b6d6bf59-xsx76',
			'cpu': 1,
			'mem': 24
		},
		{
			'namespace': 'cert-manager',
			'name': 'cert-manager-cainjector-856d4df858-csjg7',
			'cpu': 3,
			'mem': 52
		},
		{
			'namespace': 'ingress-nginx',
			'name': 'ingress-nginx-controller-59c8576d75-qbms9',
			'cpu': 3,
			'mem': 76
		},
		{
			'namespace': 'kube-system',
			'name': 'aws-node-5lmld',
			'cpu': 4,
			'mem': 41
		},
		{
			'namespace': 'kube-system',
			'name': 'cluster-autoscaler-848d4b88dc-rlvx6',
			'cpu': 2,
			'mem': 41
		},
		{
			'namespace': 'kube-system',
			'name': 'coredns-7d74b564bd-9mc2d',
			'cpu': 5,
			'mem': 8
		},
		{
			'namespace': 'kube-system',
			'name': 'kube-proxy-6zggk',
			'cpu': 1,
			'mem': 14
		},
		{
			'namespace': 'kube-system',
			'name': 'metrics-server-588cd8ddb5-r6hrq',
			'cpu': 4,
			'mem': 20
		},
		{
			'namespace': 'mon',
			'name': 'k8s-6894c9b96c-kg7fq',
			'cpu': 1,
			'mem': 7
		},
		{
			'namespace': 'mon',
			'name': 'munin-0',
			'cpu': 4,
			'mem': 66
		},
		{
			'namespace': 'mon',
			'name': 'munin-node-7cdd78b4d-qtpgc',
			'cpu': 1,
			'mem': 12
		},
	]
}

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		pods_top._print = MagicMock()

	def tearDown(t):
		mon_t.tearDown()
		pods_top._print = _bup_print

	def test_print(t):
		_bup_print('test', 'ing')

	def test_parse(t):
		t.assertDictEqual(pods_top.parse({}), {'info': {}, 'total': {}})

	def test_parse_data(t):
		t.maxDiff = None
		t.assertDictEqual(pods_top.parse(_pods), {
			'info': {
				'cert-manager': {
					'cert-manager-66b6d6bf59-xsx76': {'cpu': 1, 'mem': 24},
					'cert-manager-cainjector-856d4df858-csjg7': {'cpu': 3, 'mem': 52},
				},
				'ingress-nginx': {
					'ingress-nginx-controller-59c8576d75-qbms9': {'cpu': 3, 'mem': 76},
				},
				'kube-system': {
					'aws-node-5lmld': {'cpu': 4, 'mem': 41},
					'cluster-autoscaler-848d4b88dc-rlvx6': {'cpu': 2, 'mem': 41},
					'coredns-7d74b564bd-9mc2d': {'cpu': 5, 'mem': 8},
					'kube-proxy-6zggk': {'cpu': 1, 'mem': 14},
					'metrics-server-588cd8ddb5-r6hrq': {'cpu': 4, 'mem': 20},
				},
				'mon': {
					'k8s-6894c9b96c-kg7fq': {'cpu': 1, 'mem': 7},
					'munin-0': {'cpu': 4, 'mem': 66},
					'munin-node-7cdd78b4d-qtpgc': {'cpu': 1, 'mem': 12},
				},
			},
			'total': {
				'cert-manager': {'cpu': 4, 'mem': 76},
				'ingress-nginx': {'cpu': 3, 'mem': 76},
				'kube-system': {'cpu': 16, 'mem': 124},
				'mon': {'cpu': 6, 'mem': 85},
			},
		})

if __name__ == '__main__':
	unittest.main()
