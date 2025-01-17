# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import os

from email.headerregistry import Address

from pathlib import Path

from time import gmtime
from time import localtime
from time import tzset

QDIR   = os.getenv('ALERTS_QDIR',   '/var/opt/munin-alert')
DOMAIN = os.getenv('ALERTS_DOMAIN', 'uws.talkingpts.org')

MAILTO        = Address('munin alert',  'munin-alert',  DOMAIN)
MAILTO_REPORT = Address('munin report', 'munin-report', DOMAIN)

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

# amazon ses

SES_QDIR   = Path(QDIR) / 'amazon-ses'
MAILTO_SES = Address('infra-reports', 'infra-reports-aaaaemqdujfnolzj55j5bljebm', 'talkingpoints.slack.com')
MAILCC_SES = [
	'jeremias@talkingpts.org',
]
