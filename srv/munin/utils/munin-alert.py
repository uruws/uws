#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import fileinput
import json
import sys

from email.message import EmailMessage
from email.headerregistry import Address
from io import StringIO

def parse(stats):
	msg = EmailMessage()
	msg['From'] = Address('munin alert', 'munin-alert', 'uws.talkingpts.org')
	msg['To'] = Address('jrms', 'jeremias', 'talkingpts.org')
	msg['Subject'] = _msgSubject(stats)
	with StringIO() as c:
		_msgContent(c, stats)
		msg.set_content(c.getvalue())
		c.close()
	return msg

def _getTitle(s):
	t = s.get('title', 'NO_TITLE').split('::')
	if len(t) == 1:
		return t[0].strip()
	return t[-1].strip()

def _msgSubject(s):
	worst = s.get('worst', 'ERROR')
	host = s.get('host', 'NO_HOST')
	title = _getTitle(s)
	return f"[{worst}] {host} {title}"

def _msgContent(c, s):
	worst = s.get('worst', 'ERROR')
	group = s.get('group', 'NO_GROUP')
	host = s.get('host', 'NO_HOST')
	plugin = s.get('plugin', 'NO_PLUGIN')
	category = s.get('category', 'NO_CATEGORY')
	title = _getTitle(s)
	c.write(f"{group} :: {host} :: {plugin}\n")
	c.write('\n')
	c.write(f"{category} :: {title} :: {worst}\n")
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

def send(m):
	print('MSG:', m)

def main():
	# ~ fh = open('/home/uws/tmp/munin-run/alerts.out', 'w')
	try:
		for line in fileinput.input('-'):
			line = line.strip()
			# ~ print(line, file = fh)
			try:
				# ~ print('LINE:', line)
				stats = json.loads(line)
			except Exception as err:
				# TODO: send [ERROR] by email
				print('ERROR:', err, file = sys.stderr)
				continue
			msg = parse(stats)
			send(msg)
	except KeyboardInterrupt:
		# ~ fh.close()
		return 1
	# ~ fh.close()
	return 128

if __name__ == '__main__':
	sys.exit(main())
