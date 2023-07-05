#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from pathlib import Path

sys.path.insert(0, '/opt/munin/lib')
import alerts_conf as conf

sys.path.insert(0, '/opt/uws/lib')
import sendmail

def __loadenv():
	# ugly hack to avoid env vars in crond email headers
	fn = os.getenv('UWS_SMTPS_CONF', '').strip()
	env = {}
	if fn != '':
		fh = Path(fn)
		if fh.is_file():
			for line in fh.read_text().splitlines():
				line = line.strip()
				if line.startswith('UWS_SMTPS'):
					i = line.split('=')
					if len(i) == 2:
						k = i[0].strip()
						v = i[1].strip()
						env[k] = v
	if len(env) > 0:
		os.environ.update(env)

if __name__ == '__main__':
	__loadenv()
	sys.exit(sendmail.qdir(conf.QDIR))
