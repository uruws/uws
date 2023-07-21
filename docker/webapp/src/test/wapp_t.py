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

def mock_nqrun(cmd, env = None):
	proc = MagicMock()
	proc.returncode = 0
	return wapp.NQJob(proc)

def mock_nqrun_error(cmd, env = None):
	proc = MagicMock()
	proc.returncode = 999
	return wapp.NQJob(proc)

def mock_nqrun_fail(cmd, env = None):
	raise RuntimeError('mock_nqrun_fail')

@contextmanager
def mock(debug = False, base_url = '/'):
	with mock_start(debug = debug) as m:
		bup_response = wapp.response
		bup_request  = wapp.request
		bup_template = wapp.template
		bup_nqrun    = wapp._nqrun
		bup_base_url = wapp.base_url.strip()
		try:
			wapp.response       = m.response
			wapp.request        = m.request
			wapp.template       = m.template
			wapp._nqrun         = m.nqrun
			m.nqrun.side_effect = mock_nqrun
			wapp.base_url       = base_url.strip()
			yield m
		finally:
			wapp.response = bup_response
			wapp.request  = bup_request
			wapp.template = bup_template
			wapp._nqrun   = bup_nqrun
			wapp.base_url = bup_base_url.strip()
			mock_cleanup()
