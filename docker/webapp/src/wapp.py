# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging

from bottle  import Bottle
from logging import Logger

__all__ = [
	'Bottle',
	'Logger',
]

from pathlib import Path

log: Logger = logging.getLogger(__name__)

#
# logging
#

# https://docs.python.org/3.9/library/logging.html#logrecord-attributes
logfmt_debug = '%(pathname)s:%(lineno)d %(message)s'

def getLogger(name: str) -> logging.Logger:
	return logging.getLogger(name)

#
# bottle
#

def bottle_start(app: str):
	log.debug('bottle_start: %s', app)
	bottle.TEMPLATE_PATH = [
		Path('/opt/uws/lib/views'),
	]

#
# main
#

def start(name: str, debug: bool = False):
	if debug:
		logging.basicConfig(format = logfmt_debug, level = logging.DEBUG)
	log.debug('start: %s', name)
	bottle_start(name)
