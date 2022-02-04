# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass
from os import getenv

@dataclass
class User(object):
	name: str

	def __repr__(u) -> str:
		return u.name

def getuser() -> User:
	return User(name = getenv('USER', 'unknown'))

def user_auth(user: User, apps: list[str]) -> list[str]:
	return sorted(apps)

def user_check(user: User):
	pass
