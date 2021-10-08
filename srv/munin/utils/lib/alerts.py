# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import fileinput
import json
import os
import sys

from email.headerregistry import Address
from email.message import EmailMessage
from email.policy import SMTP
from email.utils import formatdate, make_msgid

from io import StringIO
from time import time_ns

QDIR = os.getenv('ALERTS_QDIR', '/var/opt/munin-alert')
MAIL_FROM = Address('munin alert', 'munin-alert', 'uws.talkingpts.org')
MAIL_TO = Address('jrms', 'jeremias', 'talkingpts.org')

def _msgNew():
	m = EmailMessage(policy = SMTP)
	m.set_charset('utf-8')
	m['Date'] = formatdate()
	m['Message-ID'] = make_msgid()
	return m

def _getTitle(s):
	t = s.get('title', 'NO_TITLE').split('::')
	if len(t) == 1:
		return t[0].strip()
	return t[-1].strip()

def _stateChanged(s):
	return s.get('state_changed', '') == '1'

def _msgSubject(s):
	worst = s.get('worst', 'ERROR')
	host = s.get('host', 'NO_HOST')
	title = _getTitle(s)
	if _stateChanged(s):
		return f"[{worst}] {host} {title}"
	else:
		return f"{worst}: {host} {title}"

def _msgContent(c, s, m):
	worst = s.get('worst', 'ERROR')
	group = s.get('group', 'NO_GROUP')
	host = s.get('host', 'NO_HOST')
	plugin = s.get('plugin', 'NO_PLUGIN')
	category = s.get('category', 'NO_CATEGORY')
	title = _getTitle(s)
	c.write(f"{m['Date']}\n")
	c.write('\n')
	c.write(f"{group} :: {host} :: {plugin}\n")
	c.write(f"{category} :: {title} :: {worst}\n")
	c.write('\n')
	c.write(f"state changed: {_stateChanged(s)}\n")
	c.write('\n')
	kind = worst.lower()
	if kind == 'ok' or kind == 'error':
		ok = s.get('ok', [])
		if len(ok) > 0:
			c.write('OK\n')
			for f in ok:
				c.write(f"  {f['label']}: {f['value']}\n")
		foks = s.get('foks', [])
		if len(foks) > 0:
			c.write('RECOVER\n')
			for f in foks:
				c.write(f"  {f['label']}: {f['value']}\n")
	if kind == 'warning' or kind == 'error':
		warn = s.get('warning', [])
		if len(warn) > 0:
			c.write('WARNING\n')
			for f in warn:
				c.write(f"  {f['label']}: {f['value']}\n")
	if kind == 'critical' or kind == 'error':
		crit = s.get('critical', [])
		if len(crit) > 0:
			c.write('CRITICAL\n')
			for f in crit:
				c.write(f"  {f['label']}: {f['value']}\n")
	if kind == 'unknown' or kind == 'error':
		unk = s.get('unknown', [])
		if len(unk) > 0:
			c.write('UNKNOWN\n')
			for f in unk:
				c.write(f"  {f['label']}\n")

def parse(stats):
	msg = _msgNew()
	msg['From'] = MAIL_FROM
	msg['To'] = MAIL_TO
	msg['Subject'] = _msgSubject(stats)
	with StringIO() as c:
		_msgContent(c, stats, msg)
		msg.set_content(c.getvalue())
	return msg

def nq(m):
	fn = f"{QDIR}/{time_ns()}.eml"
	try:
		with open(fn, 'wb') as fh:
			fh.write(m.as_bytes())
	except Exception as err:
		print('ERROR:', err, file = sys.stderr)
		return 9
	else:
		print(fn)
	return 0

def main():
	rc = 0
	# ~ fh = open('/home/uws/tmp/munin-run/alerts.out', 'w')
	try:
		for line in fileinput.input('-'):
			line = line.strip()
			# ~ print(line, file = fh)
			try:
				stats = json.loads(line)
			except Exception as err:
				# TODO: nq [ERROR] message
				#       or log via syslog?
				print('ERROR:', err, file = sys.stderr)
				continue
			st = nq(parse(stats))
			if st > rc:
				rc = st
	except KeyboardInterrupt:
		# ~ fh.close()
		return 1
	# ~ fh.close()
	return rc
