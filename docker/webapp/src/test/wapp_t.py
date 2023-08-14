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

def mock_cleanup(nqdir):
	rmtree(nqdir, ignore_errors = True)

def mock_nqrun(cmd, env = None):
	proc = MagicMock()
	proc.returncode = 0
	return wapp.NQJob(proc)

def mock_nqrun_error(cmd, env = None):
	proc = MagicMock()
	proc.returncode = 999
	return wapp.NQJob(proc)

class MockNQRunFail(RuntimeError):
	pass

def mock_nqrun_fail(cmd, env = None):
	raise MockNQRunFail('mock_nqrun_fail')

nqdir: str = '/opt/uws/lib/test/data/nq'

@contextmanager
def mock(debug = False, base_url = '/', nqdir = '/tmp/wappnq', mock_error = True, cleanup = True, mock_run = True):
	with mock_start(debug = debug) as m:
		bup_redirect = wapp.redirect
		bup_response = wapp.response
		bup_request  = wapp.request
		bup_template = wapp.template
		bup_nqdir    = wapp.nqdir.strip()
		bup_nqrun    = wapp._nqrun
		bup_nqsetup  = wapp._nqsetup
		bup_base_url = wapp.base_url.strip()
		bup_error    = wapp.error
		try:
			wapp.redirect       = m.redirect
			wapp.response       = m.response
			m.response.status   = 200
			wapp.request        = m.request
			m.request.path      = '/testing/'
			wapp.template       = m.template
			wapp.nqdir          = nqdir.strip()
			wapp.base_url       = base_url.strip()
			if mock_run:
				wapp._nqsetup = m.nqsetup
				wapp._nqrun = m.nqrun
				m.nqrun.side_effect = mock_nqrun
			if mock_error:
				wapp.error = m.error
			yield m
		finally:
			wapp.redirect = bup_redirect
			wapp.response = bup_response
			wapp.request  = bup_request
			wapp.template = bup_template
			wapp.nqdir    = bup_nqdir.strip()
			wapp.base_url = bup_base_url.strip()
			if mock_run:
				wapp._nqsetup = bup_nqsetup
				wapp._nqrun = bup_nqrun
			if mock_error:
				wapp.error = bup_error
			if cleanup:
				mock_cleanup(nqdir)
