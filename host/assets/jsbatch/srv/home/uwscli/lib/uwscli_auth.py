# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass, field
from os import getenv
from subprocess import getstatusoutput

import uwscli_conf as conf

EGROUPS = 40
EARGS   = 41
ECHECK  = 42
EPOD    = 43

@dataclass
class User(object):
	name:     str
	groups:   dict[str, bool] = field(default_factory = dict)
	is_admin: bool            = False

	def __repr__(u) -> str:
		return u.name

	def load_groups(u) -> int:
		cmd = f"/usr/bin/id -Gn {u.name}"
		rc, out = getstatusoutput(cmd)
		if rc == 0:
			u.groups.clear()
			for g in out.splitlines():
				g = g.strip()
				u.groups[g] = True
		if u.groups.get(conf.admin_group) is True:
			u.is_admin = True
		return rc

def getuser() -> User:
	return User(name = getenv('USER', 'nobody'))

def _check_app(user: User, group: str) -> int:
	if user.is_admin:
		return 0
	elif user.groups.get(group) is True:
		return 0
	return ECHECK

def user_auth(user: User, apps: list[str]) -> list[str]:
	if user.load_groups() != 0:
		return []
	if user.is_admin:
		return sorted(apps)
	r = {}
	for a in apps:
		groups = {}
		for g in conf.app[a].groups:
			groups[g] = True
		for g in groups.keys():
			if _check_app(user, g) == 0:
				r[a] = True
	return sorted(r.keys())

def _check_pod(user: User, pod: str) -> int:
	groups = {}
	for a in conf.app.keys():
		if conf.app[a].pod == pod:
			for g in conf.app[a].groups:
				groups[g] = True
	for g in groups.keys():
		if _check_app(user, g) == 0:
			return 0
	return EPOD

def _check_workdir(user: User, workdir: str) -> int:
	return 0

def user_check(username: str, build: str, pod: str, workdir: str) -> int:
	user = User(name = username)
	if user.load_groups() != 0:
		return EGROUPS
	if build != '':
		st = _check_app(user, build)
		if st != 0:
			return st
	if pod != '':
		st = _check_pod(user, pod)
		if st != 0:
			return st
	if workdir != '':
		st = _check_workdir(user, workdir)
		if st != 0:
			return st
	return EARGS
