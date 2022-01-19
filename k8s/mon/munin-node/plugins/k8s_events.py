# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	apiserver_init_events_total = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if sts.get(name, None) is not None:
		resource = meta.get('resource', None)
		sts[name][resource] = value
		return True
	return False

def _print(*args):
	print(*args)

# ~ def config(sts):
	# ~ mon.dbg('config k8s_events')
	# ~ cluster = mon.cluster()
	# ~ _print('multigraph k8s_events')
	# ~ _print(f"graph_title {cluster} kubernetes apiserver TLS")
	# ~ _print('graph_args --base 1000 -l 0')
	# ~ _print('graph_category k8s')
	# ~ _print('graph_vlabel number')
	# ~ _print('graph_scale yes')
	# ~ _print('errors.label errors')
	# ~ _print('errors.colour ff0000')
	# ~ _print('errors.draw AREA')
	# ~ _print('errors.min 0')
	# ~ _print('errors.type DERIVE')
	# ~ _print('errors.cdef errors,1000,/')

# ~ def report(sts):
	# ~ mon.dbg('report k8s_events')
	# ~ _print('multigraph k8s_events')
	# ~ _print('errors.value', sts['apiserver_tls_handshake_errors_total'])
