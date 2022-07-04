# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

from email.headerregistry import Address

from pathlib import Path

from time import gmtime
from time import localtime
from time import tzset

QDIR = os.getenv('ALERTS_QDIR', '/var/opt/munin-alert')

MAILTO = Address('munin alert', 'munin-alert', 'uws.talkingpts.org')
MAILTO_REPORT = Address('munin report', 'munin-report', 'uws.talkingpts.org')

# sleeping hours

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

SP_QDIR = Path(QDIR) / 'statuspage'
SP_MAILFROM = Address('munin statuspage', 'munin-statuspage', 'uws.talkingpts.org')

sp = {}
