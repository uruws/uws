# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	go_info                    = 'go_version',
	go_goroutines              = 'U',
	go_threads                 = 'U',
	process_cpu_seconds_total  = 'U',
	process_start_time_seconds = 'U',
	process_start_time_hours   = 'U',
)

def parse(name: str, meta: dict, value: float):
	global sts
	if name == 'go_info':
		sts[name] = meta.get('version', 'go_version')
	elif name == 'go_goroutines':
		sts[name] = value
	elif name == 'go_threads':
		sts[name] = value
	elif name == 'process_cpu_seconds_total':
		sts[name] = value
	elif name == 'process_start_time_seconds':
		sts[name] = value
		sts['process_start_time_hours'] = value / 60.0 / 60.0
	else:
		return False
	return True

def _print(*args):
	print(*args)
