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

_sts = {
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
		t.assertDictEqual(pods_top.parse(_pods), _sts)

	def test_config(t):
		pods_top.config(_sts)
		config = [
			# cpu total
			call('multigraph pods_top_cpu'),
			call('graph_title k8stest pods CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel millicores'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('cert_manager.label cert-manager'),
			call('cert_manager.colour COLOUR0'),
			call('cert_manager.draw AREASTACK'),
			call('cert_manager.min 0'),
			call('ingress_nginx.label ingress-nginx'),
			call('ingress_nginx.colour COLOUR1'),
			call('ingress_nginx.draw AREASTACK'),
			call('ingress_nginx.min 0'),
			call('kube_system.label kube-system'),
			call('kube_system.colour COLOUR2'),
			call('kube_system.draw AREASTACK'),
			call('kube_system.min 0'),
			call('mon.label mon'),
			call('mon.colour COLOUR3'),
			call('mon.draw AREASTACK'),
			call('mon.min 0'),
			# mem total
			call('multigraph pods_top_mem'),
			call('graph_title k8stest pods memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('graph_total total'),
			call('cert_manager.label cert-manager'),
			call('cert_manager.colour COLOUR0'),
			call('cert_manager.draw AREASTACK'),
			call('cert_manager.min 0'),
			call('ingress_nginx.label ingress-nginx'),
			call('ingress_nginx.colour COLOUR1'),
			call('ingress_nginx.draw AREASTACK'),
			call('ingress_nginx.min 0'),
			call('kube_system.label kube-system'),
			call('kube_system.colour COLOUR2'),
			call('kube_system.draw AREASTACK'),
			call('kube_system.min 0'),
			call('mon.label mon'),
			call('mon.colour COLOUR3'),
			call('mon.draw AREASTACK'),
			call('mon.min 0'),
		]
		pods_top._print.assert_has_calls(config)
		t.assertEqual(pods_top._print.call_count, len(config))

	def test_report(t):
		pods_top.report(_sts)
		report = [
			# cpu total
			call('multigraph pods_top_cpu'),
			call('cert_manager.value', 4),
			call('ingress_nginx.value', 3),
			call('kube_system.value', 16),
			call('mon.value', 6),
			# mem total
			call('multigraph pods_top_mem'),
			call('cert_manager.value', 76),
			call('ingress_nginx.value', 76),
			call('kube_system.value', 124),
			call('mon.value', 85),
		]
		pods_top._print.assert_has_calls(report)
		t.assertEqual(pods_top._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
