# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

from time import gmtime
from time import localtime

SLEEP_TZ = os.getenv('ALERTS_TZ', 'UTC')

def _gethour():
	if SLEEP_TZ != 'UTC':
		os.environ['TZ'] = SLEEP_TZ
		tzset()
		return int(localtime().tm_hour)
	return int(gmtime().tm_hour)

def sleepingHours(h = None):
	if h is None: h = _gethour()
	# from 1am to 10am (9hs per day)
	if h >= 1 and h < 10:
		return True
	return False

# statuspage
sp = {}
