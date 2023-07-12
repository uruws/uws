# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from math import ceil

import wapp

log = wapp.getLogger(__name__)

max_bytes = 3500

def _msgadd(l: list[str], lines: list[str], cmd: str, msg_id: int, msg_total: int):
	msg = '[empty]'
	if len(lines) > 0:
		msg = '\n'.join(lines)
	if msg_total <= 1:
		l.append("%s\n```%s```" % (cmd, msg))
	else:
		l.append("%s [%d/%d]\n```%s```" % (cmd, msg_id, msg_total, msg))

def parse(cmd: str, out: str) -> list[str]:
	size = len(out)
	log.debug('parse: %s - %d', cmd, size)
	l: list[str] = []
	if size == 0:
		_msgadd(l, [], cmd, 1, 1)
		return l
	x = 0
	m: list[str] = []
	lines = out.splitlines()
	msg_id = 1
	msg_total = ceil(size / max_bytes)
	for line in lines:
		lsize = len(line)
		log.debug('parse line: %d %d %d/%d', x, lsize, msg_id, msg_total)
		x += lsize
		if x >= max_bytes:
			_msgadd(l, m, cmd, msg_id, msg_total)
			x = lsize
			m.clear()
			msg_id += 1
		m.append(line)
	_msgadd(l, m, cmd, msg_id, msg_total)
	return l
