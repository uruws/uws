# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from email import policy
from email.parser import BytesParser

_eml = BytesParser(policy = policy.default)

def message(m):
	"""send an email message"""
	print('MSG:', m)
	return 128

def messageFile(fn):
	"""parse email message from file and try to send it, remove the file if
	properly sent"""
	print(fn)
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
