# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass

@dataclass
class User(object):
	pass

@dataclass
class Result(object):
	user: User

@dataclass
class Command(object):
	pass

def uwscli(cmd: Command, user: User) -> Result:
	return Result(
		user = user,
	)
