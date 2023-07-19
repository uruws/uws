#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

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

@contextmanager
def mock(debug = False):
	with mock_start(debug = debug) as m:
		bup_template = wapp.template
		try:
			wapp.template = m.template
			yield m
		finally:
			wapp.template = bup_template
