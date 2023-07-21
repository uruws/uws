# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

__all__ = [
	'url',
]

log = wapp.getLogger(__name__)

def url(path: str) -> str:
	if wapp.base_url == '/':
		return path.strip()
	return '%s%s' % (wapp.base_url, path.strip())
