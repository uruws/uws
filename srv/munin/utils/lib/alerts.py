# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import fileinput
import json
import os
import sys

from email.encoders       import encode_base64
from email.headerregistry import Address
from email.message        import EmailMessage
from email.policy         import SMTP
from email.utils          import formatdate
from email.utils          import make_msgid

from io      import StringIO
from pathlib import Path
from time    import time_ns
from socket  import gethostname

import alerts_conf as conf

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

def _msgFrom(s):
	h = s.get('host', gethostname())
	h = h.strip()
	return Address(h, 'munin-alert', h)

def _msgSubject(s):
	worst = s.get('worst', 'ERROR')
	title = _getTitle(s)
	if _stateChanged(s) or worst == 'ERROR':
		return f"[{worst}] {title}"
	else:
		return f"{worst}: {title}"

def _msgContent(c, s, m):
	worst = s.get('worst', 'ERROR')
	group = s.get('group', 'NO_GROUP')
	host = s.get('host', 'NO_HOST')
	plugin = s.get('plugin', 'NO_PLUGIN')
	category = s.get('category', 'NO_CATEGORY')
	title = _getTitle(s)
	stch = _stateChanged(s)
	c.write(f"{group} :: {category} :: {plugin}\n")
	c.write(f"{host} :: {title} :: {worst}\n")
	c.write('\n')
	c.write(f"{m['Date']}\n")
	c.write(f"state changed: {stch}\n")
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

# parse

def parse(stats):
	"""Send formatted alert stats info via internal email"""
	msg = _msgNew()
	msg['From'] = _msgFrom(stats)
	msg['To'] = conf.MAILTO
	msg['Subject'] = _msgSubject(stats)
	with StringIO() as c:
		_msgContent(c, stats, msg)
		msg.set_content(c.getvalue())
	return msg

# report

def report(stats):
	"""Send alert stats json content via internal email"""
	msg = _msgNew()
	msg['From'] = _msgFrom(stats)
	msg['To'] = conf.MAILTO_REPORT
	msg['Subject'] = _msgSubject(stats)
	try:
		with StringIO() as c:
			json.dump(stats, c, indent = 2)
			msg.set_content(c.getvalue())
	except Exception as err:
		print('ERROR:', err, file = sys.stderr)
		return None
	del msg['Content-Transfer-Encoding']
	encode_base64(msg)
	return msg

# nq

def _open(fn, mode):
	return open(fn, mode)

def _timestamp():
	return time_ns()

def nq(m, prefix = '', qdir = None):
	if m is None:
		print('ERROR: nq no message', file = sys.stderr)
		return 8
	if qdir is None:
		qdir = conf.QDIR
	fn = f"{qdir}/{_timestamp()}.eml"
	if prefix != '':
		fn = f"{qdir}/{prefix}-{_timestamp()}.eml"
	try:
		with _open(fn, 'wb') as fh:
			fh.write(m.as_bytes())
	except Exception as err:
		print('ERROR:', err, file = sys.stderr)
		return 9
	else:
		print(fn)
	return 0

# statuspage

def _sp(mailfrom, mailto, worst):
	msg = _msgNew()
	msg['From'] = mailfrom
	msg['To'] = mailto
	mailcc = conf.sp['_'].get('sp_mailcc', [])
	if len(mailcc) > 0:
		msg['Cc'] = ','.join(mailcc)
	if worst == 'OK':
		msg['Subject'] = 'UP'
		body = '=)'
	else:
		msg['Subject'] = 'DOWN'
		body = '=('
	msg.set_content(body)
	return msg

def _spmailto(cdesc, comp):
	domain = conf.sp['_'].get('sp_domain', 'localhost')
	addr = Address(cdesc, comp, domain)
	return str(addr)

def _spmailfrom(host, category, plugin):
	addr = Address(f"{host} :: {category} :: {plugin}", 'munin-statuspage', conf.DOMAIN)
	return str(addr)

def statuspage(stats):
	"""Send statuspage.io component alerts via SES mailx"""
	conf.sp_load()
	host = stats.get('host', 'NO_HOST')
	group = stats.get('group', 'NO_GROUP')
	category = stats.get('category', 'NO_CATEGORY')
	plugin = stats.get('plugin', 'NO_PLUGIN')
	worst = stats.get('worst', 'ERROR')
	if worst != 'OK' and worst != 'CRITICAL':
		return 1
	cid = f"{category}::{plugin}"
	if conf.sp.get(host, None) is not None:
		if conf.sp[host].get(group, None) is not None:
			p = Path(cid)
			for key in conf.sp[host][group].keys():
				if p.match(key):
					cfg = conf.sp[host][group].get(key)
					comp = cfg.get('component', '').strip()
					if comp == '':
						continue
					cdesc = cfg.get('component_description', '').strip()
					mailto = _spmailto(cdesc, comp)
					mailfrom = _spmailfrom(host, category, plugin)
					return nq(_sp(mailfrom, mailto, worst), qdir = conf.SP_QDIR.as_posix())
	return 2

# main

def main():
	rc = 0
	try:
		for line in fileinput.input('-'):

			line = line.strip()
			try:
				stats = json.loads(line)
			except Exception as err:
				# TODO: nq [ERROR] message
				#       or log via syslog?
				#       or even better via SES mailx?
				print('ERROR:', err, file = sys.stderr)
				continue

			worst = stats.get('worst', 'ERROR')
			stch  = _stateChanged(stats)

			# do not send OK messages if no state changed
			if not stch and worst == 'OK':
				continue

			# send report email in json format
			# ~ st = nq(report(stats), prefix = 'report')
			# ~ if st > rc:
				# ~ rc = st

			# check/avoid sysadmin sleeping hours
			# ~ if _sleepingHours() and worst != 'CRITICAL':
				# ~ # only CRITICAL messages during sysadmin sleeping hours
				# ~ continue

			# send email alert using internal smtps
			st = nq(parse(stats))
			if st > rc:
				rc = st

			# statuspage report using external smtps
			if stch:
				statuspage(stats)

	except KeyboardInterrupt:
		return 1
	return rc
