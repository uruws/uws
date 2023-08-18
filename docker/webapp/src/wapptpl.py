# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import re

import wapp

__all__ = [
	'slug',
	'url',
]

log = wapp.getLogger(__name__)

__slug_re = re.compile('\W')

def slug(s: str) -> str:
	return __slug_re.sub('_', s)

def url(*args) -> str:
	if len(args) == 0:
		return wapp.request.path.strip()
	path = '/'.join(args)
	if path.startswith('//'):
		path = path[1:]
	if wapp.base_url == '/':
		return path.strip()
	return '%s%s' % (wapp.base_url, path.strip())
