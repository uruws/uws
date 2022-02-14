# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass, field
from os import getenv

@dataclass
class User(object):
	name:   str
	groups: dict[str, bool] = field(default_factory = dict)

	def __repr__(u) -> str:
		return u.name

	def load_groups(u):
		pass

def getuser() -> User:
	return User(name = getenv('USER', 'unknown'))

def user_auth(user: User, apps: list[str]) -> list[str]:
	return sorted(apps)

def _check_build(user: User, build: str) -> int:
	return 0

def _check_pod(user: User, pod: str) -> int:
	return 0

def _check_workdir(user: User, workdir: str) -> int:
	return 0

def user_check(username: str, build: str, pod: str, workdir: str) -> int:
	user = User(name = username)
	user.load_groups()
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
	return rc
