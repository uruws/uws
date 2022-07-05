#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

sys.path.insert(0, '/opt/munin/lib')
import alerts_conf as conf

sys.path.insert(0, '/opt/uws/lib')
import sendmail

if __name__ == '__main__':
	sys.exit(sendmail.qdir(conf.QDIR))
