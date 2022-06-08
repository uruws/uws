# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass
from dataclasses import field

@dataclass
class AppUser(object):
	uid:         int
	name:        str             = ""
	groups:      dict[str, bool] = field(default_factory = dict)
	is_admin:    bool            = False
	is_operator: bool            = False
	keyid:       str             = ""
	username:    str             = ""

	def __post_init__(u):
		if u.is_admin:
			u.is_operator
		if u.username == "" and u.name != "":
			u.username = "%s@talkingpts.org" % u.name

user: dict[str, AppUser] = {}
