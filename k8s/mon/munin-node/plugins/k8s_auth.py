# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import mon

sts = dict(
	authenticated_user_requests = dict(),
	authentication_attempts = dict(),
)

def parse(name: str, meta: dict, value: float):
	global sts
	if name == 'authenticated_user_requests':
		username = meta.get('username', None)
		sts[name][username] = value
		return True
	elif name == 'authentication_attempts':
		result = meta.get('result', None)
		sts[name][result] = value
		return True
	return False

def _print(*args):
	print(*args)

def config(sts):
	mon.dbg('config k8s_auth')
	cluster = mon.cluster()
	# attempts
	_print('multigraph k8s_auth_attempts')
	_print(f"graph_title {cluster} kubernetes apiserver auth attempts")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category number')
	_print('graph_vlabel bytes')
	_print('graph_scale yes')
	color = 0
	for result in sorted(sts['authentication_attempts'].keys()):
		rid = mon.cleanfn(result)
		_print(f"{rid}.label {result}")
		_print(f"{rid}.colour COLOUR{color}")
		_print(f"{rid}.min 0")
		_print(f"{rid}.type DERIVE")
		_print(f"{rid}.cdef {rid},1000,/")
		color = mon.color(color)
	# requests
	_print('multigraph k8s_auth_requests')
	_print(f"graph_title {cluster} kubernetes apiserver auth requests")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category number')
	_print('graph_vlabel bytes')
	_print('graph_scale yes')
	color = 0
	for username in sorted(sts['authenticated_user_requests'].keys()):
		uid = mon.cleanfn(username)
		_print(f"user_{uid}.label {username}")
		_print(f"user_{uid}.colour COLOUR{color}")
		_print(f"user_{uid}.min 0")
		_print(f"user_{uid}.type DERIVE")
		_print(f"user_{uid}.cdef {uid},1000,/")
		color = mon.color(color)

def report(sts):
	mon.dbg('report k8s_auth')
	# attempts
	_print('multigraph k8s_auth_attempts')
	for result in sorted(sts['authentication_attempts'].keys()):
		rid = mon.cleanfn(result)
		_print(f"{rid}.value",
			mon.derive(sts['authentication_attempts'][result]))
	# requests
	_print('multigraph k8s_auth_requests')
	for username in sorted(sts['authenticated_user_requests'].keys()):
		uid = mon.cleanfn(username)
		_print(f"user_{uid}.value",
			mon.derive(sts['authenticated_user_requests'][username]))
