#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock, call

import mon_t

import nginx_proc

_bup_print = nginx_proc._print
_bup_sts = {}
_bup_sts.update(nginx_proc.sts)
_bup_time = nginx_proc.time

class Test(unittest.TestCase):

	def setUp(t):
		mon_t.setUp()
		nginx_proc._print = MagicMock()
		nginx_proc.time = MagicMock(return_value = 100.0)

	def tearDown(t):
		mon_t.tearDown()
		nginx_proc._print = _bup_print
		nginx_proc.sts = {}
		nginx_proc.sts.update(_bup_sts)
		nginx_proc.time = _bup_time

	def test_globals(t):
		t.assertDictEqual(nginx_proc.sts, {
			'byte': {
				'read': 'U',
				'write': 'U',
			},
			'cpu': {
				'controller': 'U',
				'total': 'U',
			},
			'mem': {
				'resident': 'U',
				'virtual': 'U',
			},
			'requests': 'U',
			'uptime': 'U',
		})

	def test_print(t):
		_bup_print('test', 'ing')

	def test_parse(t):
		t.assertFalse(nginx_proc.parse('testing', None, None))

	def test_parse_cpu(t):
		t.assertTrue(nginx_proc.parse(nginx_proc.CPU_CONTROLLER, None, 0.999))
		t.assertTrue(nginx_proc.parse(nginx_proc.CPU_TOTAL, None, 0.999))
		t.assertDictEqual(nginx_proc.sts['cpu'], {
			'controller': 0.999,
			'total': 0.999,
		})

	def test_parse_mem(t):
		t.assertTrue(nginx_proc.parse(nginx_proc.MEM_RESIDENT, None, 0.999))
		t.assertTrue(nginx_proc.parse(nginx_proc.MEM_VIRTUAL, None, 0.999))
		t.assertDictEqual(nginx_proc.sts['mem'], {
			'resident': 0.999,
			'virtual': 0.999,
		})

	def test_parse_uptime(t):
		t.assertTrue(nginx_proc.parse(nginx_proc.UPTIME, None, 99.0))
		t.assertEqual(nginx_proc.sts['uptime'], 1.0)

	def test_parse_requests(t):
		t.assertTrue(nginx_proc.parse(nginx_proc.REQ_TOTAL, None, 99.0))
		t.assertEqual(nginx_proc.sts['requests'], 99.0)

	def test_parse_bytes(t):
		t.assertTrue(nginx_proc.parse(nginx_proc.READ_TOTAL, None, 0.999))
		t.assertTrue(nginx_proc.parse(nginx_proc.WRITE_TOTAL, None, 0.999))
		t.assertDictEqual(nginx_proc.sts['byte'], {'read': 0.999, 'write': 0.999})

	def test_config(t):
		nginx_proc.config({})
		config = [
			# cpu
			call('multigraph nginx_proc_cpu'),
			call('graph_title CPU usage'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx'),
			call('graph_vlabel time per second'),
			call('graph_scale no'),
			call('controller.label controller'),
			call('controller.colour COLOUR0'),
			call('controller.type DERIVE'),
			call('controller.min 0'),
			call('controller.cdef controller,1000,/'),
			call('total.label total'),
			call('total.colour COLOUR1'),
			call('total.type DERIVE'),
			call('total.min 0'),
			call('total.cdef total,1000,/'),
			# mem
			call('multigraph nginx_proc_mem'),
			call('graph_title Memory usage'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category nginx'),
			call('graph_vlabel bytes'),
			call('graph_scale yes'),
			call('resident.label resident'),
			call('resident.colour COLOUR0'),
			call('resident.draw AREA'),
			call('resident.min 0'),
			call('virtual.label virtual'),
			call('virtual.colour COLOUR1'),
			call('virtual.draw AREA'),
			call('virtual.min 0'),
			# uptime
			call('multigraph nginx_proc_uptime'),
			call('graph_title Uptime'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx'),
			call('graph_vlabel hours'),
			call('graph_scale no'),
			call('uptime.label uptime'),
			call('uptime.colour COLOUR0'),
			call('uptime.draw AREA'),
			call('uptime.min 0'),
			# requests total
			call('multigraph nginx_proc_requests'),
			call('graph_title Requests total'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_req'),
			call('graph_vlabel number'),
			call('graph_scale yes'),
			call('requests.label requests'),
			call('requests.colour COLOUR0'),
			call('requests.min 0'),
			# requests counter
			call('multigraph nginx_proc_requests.counter'),
			call('graph_title Requests'),
			call('graph_args --base 1000 -l 0'),
			call('graph_category nginx_req'),
			call('graph_vlabel number per second'),
			call('graph_scale yes'),
			call('requests.label requests'),
			call('requests.colour COLOUR0'),
			call('requests.type DERIVE'),
			call('requests.min 0'),
			call('requests.cdef requests,1000,/'),
			# bytes total
			call('multigraph nginx_proc_bytes'),
			call('graph_title Bytes read/write total'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category nginx'),
			call('graph_vlabel read(-)/write(+) per second'),
			call('graph_scale yes'),
			call('read.label bytes'),
			call('read.graph no'),
			call('read.min 0'),
			call('write.label bytes'),
			call('write.negative read'),
			call('write.min 0'),
			# bytes counter
			call('multigraph nginx_proc_bytes.counter'),
			call('graph_title Bytes read/write'),
			call('graph_args --base 1024 -l 0'),
			call('graph_category nginx'),
			call('graph_vlabel read(-)/write(+) per second'),
			call('graph_scale yes'),
			call('read.label bytes'),
			call('read.type DERIVE'),
			call('read.graph no'),
			call('read.min 0'),
			call('read.cdef read,1000,/'),
			call('write.label bytes'),
			call('write.type DERIVE'),
			call('write.negative read'),
			call('write.min 0'),
			call('write.cdef write,1000,/'),
		]
		nginx_proc._print.assert_has_calls(config)
		t.assertEqual(nginx_proc._print.call_count, len(config))

if __name__ == '__main__':
	unittest.main()
