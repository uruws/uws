# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	aggregator_unavailable_apiservice_total = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		reason = meta.get('reason', None)
		n = meta.get('name', None)
		if sts[name].get(reason, None) is None:
			sts[name][reason] = dict()
		sts[name][reason][n] = value
		return True
	return False

def _print(*args):
	print(*args)
