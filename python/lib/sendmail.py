# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from email import policy
from email.parser import BytesParser

_eml = BytesParser(policy = policy.default)

def message(m):
	print('MSG:', m)
	return 128

def messageFile(fn):
	print(fn)
	with open(fn, 'rb') as fh:
		try:
			msg = _eml.parse(fh)
		except Exception as err:
			print('ERROR:', err, file = sys.stderr)
			return 1
	return message(msg)

def qdir(d):
	rc = 0
	for n in os.listdir(d):
		if n.endswith('.eml'):
			fn = os.path.join(d, n)
			st = messageFile(fn)
			if st > rc:
				rc = st
	return rc
