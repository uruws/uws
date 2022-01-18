# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

from time import time

sts = dict(
	go_version        = 'go_version',
	goroutines        = 'U',
	threads           = 'U',
	cpu_seconds_total = 'U',
	uptime_hours      = 'U',
)

def parse(name: str, meta: dict, value: float):
	global sts
	if name == 'go_info':
		sts['go_version'] = meta.get('version', 'go_version')
	elif name == 'go_goroutines':
		sts['goroutines'] = value
	elif name == 'go_threads':
		sts['threads'] = value
	elif name == 'process_cpu_seconds_total':
		sts['cpu_seconds_total'] = value
	elif name == 'process_start_time_seconds':
		sts['uptime_hours'] = value / 60.0 / 60.0
	else:
		return False
	return True

def _print(*args):
	print(*args)
