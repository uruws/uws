# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging

from bottle import Bottle # type: ignore

from logging import Logger

__all__ = [
	'Bottle',
	'Logger',
]

#
# logging
#

# https://docs.python.org/3.9/library/logging.html#logrecord-attributes
logfmt_debug = '%(pathname)s:%(lineno)d %(message)s'

def getLogger(name: str) -> logging.Logger:
	return logging.getLogger(name)

#
# main
#

def start(debug: bool):
	if debug:
		logging.basicConfig(format = logfmt_debug, level = logging.DEBUG)
