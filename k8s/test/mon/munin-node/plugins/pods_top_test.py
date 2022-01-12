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
	'cert-manager': {'count': 2, 'cpu': 4, 'mem': 76},
	'ingress-nginx': {'count': 1, 'cpu': 3, 'mem': 76},
	'kube-system': {'count': 5, 'cpu': 16, 'mem': 124},
	'mon': {'count': 3, 'cpu': 6, 'mem': 85},
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
		t.assertDictEqual(pods_top.parse({}), {})

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
			call('cert_manager.label cert-manager', '(2)'),
			call('cert_manager.colour COLOUR0'),
			call('cert_manager.draw AREASTACK'),
			call('cert_manager.min 0'),
			call('ingress_nginx.label ingress-nginx', '(1)'),
			call('ingress_nginx.colour COLOUR1'),
			call('ingress_nginx.draw AREASTACK'),
			call('ingress_nginx.min 0'),
			call('kube_system.label kube-system', '(5)'),
			call('kube_system.colour COLOUR2'),
			call('kube_system.draw AREASTACK'),
			call('kube_system.min 0'),
			call('mon.label mon', '(3)'),
			call('mon.colour COLOUR3'),
			call('mon.draw AREASTACK'),
			call('mon.min 0'),
			call('ztotal.label total'),
			call('ztotal.colour 000000'),
			call('ztotal.draw LINE1'),
			call('ztotal.min 0'),
			# namespace cpu
			call('multigraph pods_top_cpu.cert_manager'),
			call('graph_title k8stest cert_manager pods CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel millicores'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(2)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			call('multigraph pods_top_cpu.ingress_nginx'),
			call('graph_title k8stest ingress_nginx pods CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel millicores'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(1)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			call('multigraph pods_top_cpu.kube_system'),
			call('graph_title k8stest kube_system pods CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel millicores'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(5)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			call('multigraph pods_top_cpu.mon'),
			call('graph_title k8stest mon pods CPU'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel millicores'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(3)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			# mem total
			call('multigraph pods_top_mem'),
			call('graph_title k8stest pods memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('cert_manager.label cert-manager', '(2)'),
			call('cert_manager.colour COLOUR0'),
			call('cert_manager.draw AREASTACK'),
			call('cert_manager.min 0'),
			call('ingress_nginx.label ingress-nginx', '(1)'),
			call('ingress_nginx.colour COLOUR1'),
			call('ingress_nginx.draw AREASTACK'),
			call('ingress_nginx.min 0'),
			call('kube_system.label kube-system', '(5)'),
			call('kube_system.colour COLOUR2'),
			call('kube_system.draw AREASTACK'),
			call('kube_system.min 0'),
			call('mon.label mon', '(3)'),
			call('mon.colour COLOUR3'),
			call('mon.draw AREASTACK'),
			call('mon.min 0'),
			call('ztotal.label total'),
			call('ztotal.colour 000000'),
			call('ztotal.draw LINE1'),
			call('ztotal.min 0'),
			# namespace mem
			call('multigraph pods_top_mem.cert_manager'),
			call('graph_title k8stest cert_manager pods memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(2)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			call('multigraph pods_top_mem.ingress_nginx'),
			call('graph_title k8stest ingress_nginx pods memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(1)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			call('multigraph pods_top_mem.kube_system'),
			call('graph_title k8stest kube_system pods memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(5)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
			call('multigraph pods_top_mem.mon'),
			call('graph_title k8stest mon pods memory'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category top'),
			call('graph_vlabel MiB'),
			call('graph_printf %3.0lf'),
			call('graph_scale yes'),
			call('f0_total.label total', '(3)'),
			call('f0_total.colour COLOUR0'),
			call('f0_total.draw AREASTACK'),
			call('f0_total.min 0'),
			call('f1_avg.label average'),
			call('f1_avg.colour COLOUR1'),
			call('f1_avg.draw LINE1'),
			call('f1_avg.min 0'),
		]
		pods_top._print.assert_has_calls(config)
		t.assertEqual(pods_top._print.call_count, len(config))

	def test_report(t):
		x = dict()
		x.update(_sts)
		x['test'] = dict()
		pods_top.report(x)
		report = [
			# cpu total
			call('multigraph pods_top_cpu'),
			call('cert_manager.value', 4),
			call('ingress_nginx.value', 3),
			call('kube_system.value', 16),
			call('mon.value', 6),
			call('test.value', 'U'),
			call('ztotal.value', 29),
			# namespace cpu
			call('multigraph pods_top_cpu.cert_manager'),
			call('f0_total.value', 4),
			call('f1_avg.value', 2.0),
			call('multigraph pods_top_cpu.ingress_nginx'),
			call('f0_total.value', 3),
			call('f1_avg.value', 3.0),
			call('multigraph pods_top_cpu.kube_system'),
			call('f0_total.value', 16),
			call('f1_avg.value', 3.2),
			call('multigraph pods_top_cpu.mon'),
			call('f0_total.value', 6),
			call('f1_avg.value', 2.0),
			call('multigraph pods_top_cpu.test'),
			call('f0_total.value', 'U'),
			call('f1_avg.value', 'U'),
			# mem total
			call('multigraph pods_top_mem'),
			call('cert_manager.value', 76),
			call('ingress_nginx.value', 76),
			call('kube_system.value', 124),
			call('mon.value', 85),
			call('test.value', 'U'),
			call('ztotal.value', 361),
			# namespace mem
			call('multigraph pods_top_mem.cert_manager'),
			call('f0_total.value', 76),
			call('f1_avg.value', 38.0),
			call('multigraph pods_top_mem.ingress_nginx'),
			call('f0_total.value', 76),
			call('f1_avg.value', 76.0),
			call('multigraph pods_top_mem.kube_system'),
			call('f0_total.value', 124),
			call('f1_avg.value', 24.8),
			call('multigraph pods_top_mem.mon'),
			call('f0_total.value', 85),
			call('f1_avg.value', 28.333333333333332),
			call('multigraph pods_top_mem.test'),
			call('f0_total.value', 'U'),
			call('f1_avg.value', 'U'),
		]
		pods_top._print.assert_has_calls(report)
		t.assertEqual(pods_top._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
