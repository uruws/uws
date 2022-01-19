# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	etcd_db_total_size_in_bytes = 'U',
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		sts[name] = value
		return True
	return False

def _print(*args):
	print(*args)
