# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

def messageFile(fn):
	print(fn)
	return 0

def qdir(d):
	rc = 0
	for n in os.listdir(d):
		if n.endswith('.eml'):
			fn = os.path.join(d, n)
			st = messageFile(fn)
			if st > rc:
				rc = st
	return rc
