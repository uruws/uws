# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	apiextensions_openapi_v2_regeneration_count = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		reason = meta.get('reason', None)
		crd = meta.get('crd', None)
		if sts[name].get(reason, None) is None:
			sts[name][reason] = dict()
		sts[name][reason][crd] = value
		return True
	return False

def _print(*args):
	print(*args)
