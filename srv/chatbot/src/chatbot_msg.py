# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging

from math import ceil

log = logging.getLogger(__name__)

lines_split = 30

def _msgadd(l: list[str], lines: list[str], cmd: str, msg_id: int, msg_total: int):
	if msg_total == 1:
		l.append("%s\n```%s```" % (cmd, '\n'.join(lines)))
	else:
		l.append("%s [%d/%d]\n```%s```" % (cmd, msg_id, msg_total, '\n'.join(lines)))

def parse(cmd: str, out: str) -> list[str]:
	log.debug('parse: %s - %d', cmd, len(out))
	i = 0
	l: list[str] = []
	m: list[str] = []
	lines = out.splitlines()
	lines_total = len(lines)
	msg_id = 1
	msg_total = ceil(lines_total / lines_split)
	for line in lines:
		log.debug('parse line: %d %d %d/%d', i, len(line), msg_id, msg_total)
		if i == lines_split:
			_msgadd(l, m, cmd, msg_id, msg_total)
			i = 0
			m.clear()
			msg_id += 1
		m.append(line)
		i += 1
	_msgadd(l, m, cmd, msg_id, msg_total)
	if len(l) == 0:
		return ['[empty]']
	return l
