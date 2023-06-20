# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging

log = logging.getLogger(__name__)

lines_split = 30

def parse(out: str) -> list[str]:
	log.debug('parse: %d', len(out))
	l = []
	i = 0
	m = []
	for line in out.splitlines():
		log.debug('parse line(%d): %d', i, len(line))
		if i == lines_split:
			l.append('\n'.join(m))
			i = 0
			m.clear()
		m.append(line)
		i += 1
	l.append('\n'.join(m))
	if len(l) == 0:
		return ['[empty]']
	return l
