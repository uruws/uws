# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	requests = dict(),
	attempts = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if name == 'authenticated_user_requests':
		username = meta.get('username', None)
		sts['requests'][username] = value
		return True
	elif name == 'authentication_attempts':
		result = meta.get('result', None)
		sts['attempts'][result] = value
		return True
	return False

def _print(*args):
	print(*args)
