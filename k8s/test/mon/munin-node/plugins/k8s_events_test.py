#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t
import mon_metrics

import k8s_events

_bup_print = k8s_events._print
_bup_sts = k8s_events.sts.copy()

_metrics_fn = '/go/src/k8s/mon/testdata/k8s_metrics.txt'
_sts = dict(
	apiserver_init_events_total = {
		'*apps.DaemonSet':                         4.0,
		'*apps.ReplicaSet':                        7.0,
		'*certificates.CertificateSigningRequest': 37.0,
		'*coordination.Lease':                     95.0,
		'*core.ConfigMap':                         641891.0,
		'*core.Endpoints':                         134.0,
		'*core.Node':                              6416.0,
		'*core.Pod':                               4775.0,
		'*core.Secret':                            2157.0,
		'*discovery.EndpointSlice':                3.0,
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
		k8s_events._print = MagicMock()
		k8s_events.sts = _bup_sts.copy()

	def tearDown(t):
		mon_t.tearDown()
		k8s_events._print = _bup_print

	def test_globals(t):
		t.assertDictEqual(k8s_events.sts, dict(
			apiserver_init_events_total = dict(),
		))

	def test_print(t):
		_bup_print('testing', '...')

	def test_parse(t):
		t.assertFalse(k8s_events.parse('testing', None, None))

	def test_parse_data(t):
		t.maxDiff = None
		for name, meta, value in t.metrics:
			if _bup_sts.get(name, None) is not None:
				t.assertTrue(k8s_events.parse(name, meta, value))
		t.assertDictEqual(k8s_events.sts, _sts)

	def test_config(t):
		k8s_events.config(_sts)
		config = [
			call('multigraph k8s_events'),
			call('graph_title k8stest kubernetes events'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category k8s'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('event__apps_DaemonSet.label *apps.DaemonSet'),
			call('event__apps_DaemonSet.colour COLOUR0'),
			call('event__apps_DaemonSet.draw AREA'),
			call('event__apps_DaemonSet.min 0'),
			call('event__apps_DaemonSet.type DERIVE'),
			call('event__apps_DaemonSet.cdef event__apps_DaemonSet,1000,/'),
			call('event__apps_ReplicaSet.label *apps.ReplicaSet'),
			call('event__apps_ReplicaSet.colour COLOUR1'),
			call('event__apps_ReplicaSet.draw AREA'),
			call('event__apps_ReplicaSet.min 0'),
			call('event__apps_ReplicaSet.type DERIVE'),
			call('event__apps_ReplicaSet.cdef event__apps_ReplicaSet,1000,/'),
			call('event__certificates_CertificateSigningRequest.label *certificates.CertificateSigningRequest'),
			call('event__certificates_CertificateSigningRequest.colour COLOUR2'),
			call('event__certificates_CertificateSigningRequest.draw AREA'),
			call('event__certificates_CertificateSigningRequest.min 0'),
			call('event__certificates_CertificateSigningRequest.type DERIVE'),
			call('event__certificates_CertificateSigningRequest.cdef event__certificates_CertificateSigningRequest,1000,/'),
			call('event__coordination_Lease.label *coordination.Lease'),
			call('event__coordination_Lease.colour COLOUR3'),
			call('event__coordination_Lease.draw AREA'),
			call('event__coordination_Lease.min 0'),
			call('event__coordination_Lease.type DERIVE'),
			call('event__coordination_Lease.cdef event__coordination_Lease,1000,/'),
			call('event__core_ConfigMap.label *core.ConfigMap'),
			call('event__core_ConfigMap.colour COLOUR4'),
			call('event__core_ConfigMap.draw AREA'),
			call('event__core_ConfigMap.min 0'),
			call('event__core_ConfigMap.type DERIVE'),
			call('event__core_ConfigMap.cdef event__core_ConfigMap,1000,/'),
			call('event__core_Endpoints.label *core.Endpoints'),
			call('event__core_Endpoints.colour COLOUR5'),
			call('event__core_Endpoints.draw AREA'),
			call('event__core_Endpoints.min 0'),
			call('event__core_Endpoints.type DERIVE'),
			call('event__core_Endpoints.cdef event__core_Endpoints,1000,/'),
			call('event__core_Node.label *core.Node'),
			call('event__core_Node.colour COLOUR6'),
			call('event__core_Node.draw AREA'),
			call('event__core_Node.min 0'),
			call('event__core_Node.type DERIVE'),
			call('event__core_Node.cdef event__core_Node,1000,/'),
			call('event__core_Pod.label *core.Pod'),
			call('event__core_Pod.colour COLOUR7'),
			call('event__core_Pod.draw AREA'),
			call('event__core_Pod.min 0'),
			call('event__core_Pod.type DERIVE'),
			call('event__core_Pod.cdef event__core_Pod,1000,/'),
			call('event__core_Secret.label *core.Secret'),
			call('event__core_Secret.colour COLOUR8'),
			call('event__core_Secret.draw AREA'),
			call('event__core_Secret.min 0'),
			call('event__core_Secret.type DERIVE'),
			call('event__core_Secret.cdef event__core_Secret,1000,/'),
			call('event__discovery_EndpointSlice.label *discovery.EndpointSlice'),
			call('event__discovery_EndpointSlice.colour COLOUR9'),
			call('event__discovery_EndpointSlice.draw AREA'),
			call('event__discovery_EndpointSlice.min 0'),
			call('event__discovery_EndpointSlice.type DERIVE'),
			call('event__discovery_EndpointSlice.cdef event__discovery_EndpointSlice,1000,/'),
		]
		k8s_events._print.assert_has_calls(config)
		t.assertEqual(k8s_events._print.call_count, len(config))

	def test_report(t):
		k8s_events.report(_sts)
		report = [
			call('multigraph k8s_events'),
			call('event__apps_DaemonSet.value', 4000),
			call('event__apps_ReplicaSet.value', 7000),
			call('event__certificates_CertificateSigningRequest.value', 37000),
			call('event__coordination_Lease.value', 95000),
			call('event__core_ConfigMap.value', 641891000),
			call('event__core_Endpoints.value', 134000),
			call('event__core_Node.value', 6416000),
			call('event__core_Pod.value', 4775000),
			call('event__core_Secret.value', 2157000),
			call('event__discovery_EndpointSlice.value', 3000),
		]
		k8s_events._print.assert_has_calls(report)
		t.assertEqual(k8s_events._print.call_count, len(report))

if __name__ == '__main__':
	unittest.main()
