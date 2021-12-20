#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

from unittest.mock import MagicMock

import mon

_bup_print = mon._print
_bup_cacheSet = mon.cacheSet
_bup_cacheGet = mon.cacheGet

def setUp():
	mon._print = MagicMock()
	mon._cluster = 'k8stest'
	mon.cacheSet = MagicMock()
	mon.cacheGet = MagicMock(return_value = None)

def tearDown():
	mon._print = None
	mon._print = _bup_print
	mon.cacheSet = _bup_cacheSet
	mon.cacheGet = _bup_cacheGet

@contextmanager
def mock_openfn(fail = None, fh = None):
	__bup = mon._openfn
	def __open(fn, mode):
		if fail is not None:
			raise fail
		return fh
	try:
		mon._openfn = MagicMock(side_effect = __open)
		yield
	finally:
		mon._openfn = __bup
