#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

from shutil import rmtree

import wapp

@contextmanager
def mock_start(debug = False):
	m = MagicMock()
	bup_debug   = wapp.debug
	bup_logging = wapp.logging
	try:
		wapp.debug   = debug
		wapp.logging = m.logging
		yield m
	finally:
		wapp.debug   = bup_debug
		wapp.logging = bup_logging

def mock_cleanup():
	rmtree(wapp.nqdir, ignore_errors = True)

@contextmanager
def mock(debug = False):
	with mock_start(debug = debug) as m:
		bup_response = wapp.response
		bup_request  = wapp.request
		bup_template = wapp.template
		bup_nqrun    = wapp._nqrun
		try:
			wapp.response = m.response
			wapp.request  = m.request
			wapp.template = m.template
			wapp._nqrun   = m.nqrun
			yield m
		finally:
			wapp.response = bup_response
			wapp.request  = bup_request
			wapp.template = bup_template
			wapp._nqrun   = bup_nqrun
			mock_cleanup()
