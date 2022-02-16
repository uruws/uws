# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass, field
from os import getenv
from subprocess import getstatusoutput

import uwscli_conf as conf
import uwscli_log as log

EGROUPS = 40
EARGS   = 41
ECHECK  = 42
EPOD    = 43
EWKDIR  = 44

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
			for g in out.strip().split():
				g = g.strip()
				u.groups[g] = True
		if u.groups.get(conf.admin_group) is True:
			u.is_admin = True
		return rc

def getuser() -> User:
	return User(name = getenv('USER', 'nobody'))

def _check_app(user: User, group: str) -> int:
	log.debug(user, group, user.groups)
	if user.is_admin:
		log.debug(user, 'is admin')
		return 0
	elif user.groups.get(group) is True:
		log.debug(user, 'auth group:', group)
		return 0
	log.debug(user, 'no auth')
	return ECHECK

def user_auth(user: User, apps: list[str]) -> list[str]:
	if user.load_groups() != 0:
		return []
	if user.is_admin:
		return sorted(apps)
	r = {}
	groups: dict[str, bool] = {}
	for a in apps:
		for g in conf.app[a].groups:
			if not groups.get(g, False):
				if _check_app(user, g) == 0:
					r[a] = True
				groups[g] = True
	return sorted(r.keys())

def _check_pod(user: User, pod: str) -> int:
	groups: dict[str, bool] = {}
	for a in conf.app.keys():
		# app pod
		if conf.app[a].pod == pod:
			for g in conf.app[a].groups:
				if not groups.get(g, False):
					if _check_app(user, g) == 0:
						return 0
					groups[g] = True
	return EPOD

def _check_workdir(user: User, workdir: str) -> int:
	groups: dict[str, bool] = {}
	for a in conf.app.keys():
		# app build dir
		wd = conf.app[a].build.dir
		if wd != '' and wd == workdir:
			for g in conf.app[a].groups:
				if not groups.get(g, False):
					if _check_app(user, g) == 0:
						return 0
					groups[g] = True
	return EWKDIR

def user_check(username: str, build: str, pod: str, workdir: str) -> int:
	user = User(name = username)
	if user.load_groups() != 0:
		log.error('[ERROR] user load groups:', username)
		return EGROUPS
	if build != '':
		log.debug(user, 'build:', build)
		st = _check_app(user, build)
		if st != 0:
			log.error('[ERROR] user:', user, '- build:', build)
		return st
	if pod != '':
		log.debug(user, 'pod:', pod)
		st = _check_pod(user, pod)
		if st != 0:
			log.error('[ERROR] user:', user, '- pod:', pod)
		return st
	if workdir != '':
		log.debug(user, 'workdir:', workdir)
		st = _check_workdir(user, workdir)
		if st != 0:
			log.error('[ERROR] user:', user, '- workdir:', workdir)
		return st
	return EARGS
