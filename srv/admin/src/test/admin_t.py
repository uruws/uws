# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from contextlib import contextmanager

import wapp_t
import admin_test_conf

@contextmanager
def mock():
	try:
		with wapp_t.mock() as m:
			admin_test_conf.setup()
			yield m
	finally:
		admin_test_conf.teardown()
