# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass, field
from os import getenv
from subprocess import getstatusoutput

@dataclass
class User(object):
	name:   str
	groups: dict[str, bool] = field(default_factory = dict)

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
		return rc

def getuser() -> User:
	return User(name = getenv('USER', 'unknown'))

def user_auth(user: User, apps: list[str]) -> list[str]:
	if user.load_groups() != 0:
		return []
	return [a for a in sorted(apps) if user.groups.get(a) is True]

EGROUPS = 40
ECHECK  = 41

def _check_build(user: User, build: str) -> int:
	return 0

def _check_pod(user: User, pod: str) -> int:
	return 0

def _check_workdir(user: User, workdir: str) -> int:
	return 0

def user_check(username: str, build: str, pod: str, workdir: str) -> int:
	user = User(name = username)
	if user.load_groups() != 0:
		return EGROUPS
	rc = 0
	if build != '':
		st = _check_build(user, build)
		if st != 0: rc += 1
	if pod != '':
		st = _check_pod(user, pod)
		if st != 0: rc += 1
	if workdir != '':
		st = _check_workdir(user, workdir)
		if st != 0: rc += 1
	if rc != 0:
		return ECHECK
	return 0
