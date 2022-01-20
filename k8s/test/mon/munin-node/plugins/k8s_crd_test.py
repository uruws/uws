#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_crd

_bup_print = k8s_crd._print
_bup_sts = k8s_crd.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	apiextensions_openapi_v2_regeneration_count = {
		'update': {
			'certificates.cert-manager.io':    0.0,
			'challenges.acme.cert-manager.io': 0.0,
			'clusterissuers.cert-manager.io':  0.0,
			'issuers.cert-manager.io':         0.0,
		},
	},
)

class Test(unittest.TestCase):
	metrics = None

	@classmethod
	def setUpClass(k):
		with open(_metrics_fn, 'rb') as fh:
			k.metrics = list(mon_metrics._metrics_parse(fh))

	def setUp(t):
		mon_t.setUp()
		k8s_crd._print = MagicMock()
		k8s_crd.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_crd._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_crd.sts, dict(
			apiextensions_openapi_v2_regeneration_count = dict(),
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_crd.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_crd.parse(name, meta, value))
		t.assertDictEqual(k8s_crd.sts, _sts)

	def test_config(t):
		k8s_crd.config(_sts)
		config = [
			call('multigraph k8s_crd'),
			call('graph_title k8stest k8s api CRD regeneration'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('update_certificates_cert_manager_io.label update certificates.cert-manager.io'),
			call('update_certificates_cert_manager_io.colour COLOUR0'),
			call('update_certificates_cert_manager_io.min 0'),
			call('update_certificates_cert_manager_io.type DERIVE'),
			call('update_certificates_cert_manager_io.cdef update_certificates_cert_manager_io,1000,/'),
			call('update_challenges_acme_cert_manager_io.label update challenges.acme.cert-manager.io'),
			call('update_challenges_acme_cert_manager_io.colour COLOUR1'),
			call('update_challenges_acme_cert_manager_io.min 0'),
			call('update_challenges_acme_cert_manager_io.type DERIVE'),
			call('update_challenges_acme_cert_manager_io.cdef update_challenges_acme_cert_manager_io,1000,/'),
			call('update_clusterissuers_cert_manager_io.label update clusterissuers.cert-manager.io'),
			call('update_clusterissuers_cert_manager_io.colour COLOUR2'),
			call('update_clusterissuers_cert_manager_io.min 0'),
			call('update_clusterissuers_cert_manager_io.type DERIVE'),
			call('update_clusterissuers_cert_manager_io.cdef update_clusterissuers_cert_manager_io,1000,/'),
			call('update_issuers_cert_manager_io.label update issuers.cert-manager.io'),
			call('update_issuers_cert_manager_io.colour COLOUR3'),
			call('update_issuers_cert_manager_io.min 0'),
			call('update_issuers_cert_manager_io.type DERIVE'),
			call('update_issuers_cert_manager_io.cdef update_issuers_cert_manager_io,1000,/'),
		]
		k8s_crd._print.assert_has_calls(config)
		t.assertEqual(k8s_crd._print.call_count, len(config))

	def test_report(t):
		k8s_crd.report(_sts)
		report = [
			call('multigraph k8s_crd'),
			call('update_certificates_cert_manager_io.value', 0),
			call('update_challenges_acme_cert_manager_io.value', 0),
			call('update_clusterissuers_cert_manager_io.value', 0),
			call('update_issuers_cert_manager_io.value', 0),
		]
		k8s_crd._print.assert_has_calls(report)
		t.assertEqual(k8s_crd._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
