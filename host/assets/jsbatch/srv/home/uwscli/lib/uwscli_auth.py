# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import getenv

def getuser() -> str:
	return getenv('USER', 'unknown')

def user_auth(user: str, apps: list[str]) -> list[str]:
	return sorted(apps)

def user_check(user: str):
	pass
