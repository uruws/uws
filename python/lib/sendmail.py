# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from email import policy
from email.parser import BytesParser

from smtplib import SMTP_SSL

SMTPS_SERVER = os.getenv('UWS_SMTPS', '127.0.0.1')
SMTPS_PORT = os.getenv('UWS_SMTPS_PORT', 465)
SMTPS_TIMEOUT = os.getenv('UWS_SMTPS_TIMEOUT', 7)
SMTPS_CERT = os.getenv('UWS_SMTPS_CERT', '/etc/ssl/certs/ssl-cert-snakeoil.pem')
SMTPS_KEY = os.getenv('UWS_SMTPS_KEY', '/etc/ssl/private/ssl-cert-snakeoil.key')

def _smtpServer():
	return SMTP_SSL(
		host = SMTPS_SERVER,
		port = SMTPS_PORT,
		timeout = SMTPS_TIMEOUT,
		certfile = SMTPS_CERT,
		keyfile = SMTPS_KEY,
	)

def message(m):
	"""send an email message"""
	try:
		with _smtpServer() as s:
			s.send_message(m)
	except Exception as err:
		print('ERROR: smtps', SMTPS_SERVER, err, file = sys.stderr)
		return 9
	return 0

_eml = BytesParser(policy = policy.default)

def messageFile(fn):
	"""parse email message from file and try to send it, remove the file if
	properly sent"""
	with open(fn, 'rb') as fh:
		try:
			msg = _eml.parse(fh)
		except Exception as err:
			print('ERROR:', err, file = sys.stderr)
			return 1
	rc = message(msg)
	if rc == 0:
		try:
			os.unlink(fn)
		except Exception as err:
			print('ERROR:', err, file = sys.stderr)
			return 2
	return rc

def qdir(d):
	"""search dir for .eml files and pass them to messageFile"""
	rc = 0
	for n in os.listdir(d):
		if n.endswith('.eml'):
			fn = os.path.join(d, n)
			st = messageFile(fn)
			if st > rc:
				rc = st
	return rc
