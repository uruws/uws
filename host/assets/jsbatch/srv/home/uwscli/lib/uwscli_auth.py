# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from dataclasses import dataclass, field
from os import getenv
from subprocess import getstatusoutput

import uwscli_conf as conf
import uwscli_log as log

EGROUPS = 40
EOPS    = 41
EARGS   = 42
ECHECK  = 43
EPOD    = 44
EWKDIR  = 45

@dataclass
class User(object):
	name:        str
	groups:      dict[str, bool] = field(default_factory = dict)
	is_admin:    bool            = False
	is_operator: bool            = False

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
		# operator
		if u.groups.get(conf.operator_group) is True:
			u.is_operator = True
		# admin
		if u.groups.get(conf.admin_group) is True:
			u.is_admin = True
		# root
		elif u.name == 'root':
			# make root an admin too for uwscli_setup.py stuff
			u.is_operator = True
			u.is_admin = True
		return rc

def getuser() -> User:
	return User(name = getenv('USER', 'nobody'))

def _check_app(user: User, group: str, ops: str = '') -> int:
	log.debug(user, group, ops)
	if user.is_admin:
		log.debug(user, 'is admin')
		return 0
	elif user.groups.get(group) is True:
		log.debug(user, 'auth group:', group)
		if ops != '':
			if user.is_operator:
				log.debug(user, 'is operator:', ops)
				return 0
		else:
			return 0
	log.debug(user, 'no auth')
	return ECHECK

def user_auth(user: User, apps: list[str]) -> list[str]:
	if user.load_groups() != 0:
		return []
	if user.is_admin:
		return sorted(apps)
	r = {}
	done: dict[str, bool] = {}
	for a in apps:
		for g in conf.app[a].groups:
			x = done.get(g, None)
			if x is True:
				r[a] = True
				continue
			elif x is False:
				continue
			if _check_app(user, g) == 0:
				r[a] = True
				done[g] = True
			else:
				done[g] = False
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
		if conf.app[a].build.type == 'pack':
			wd = conf.app[a].build.src
		if wd != '' and wd == workdir:
			for g in conf.app[a].groups:
				if not groups.get(g, False):
					if _check_app(user, g) == 0:
						return 0
					groups[g] = True
	return EWKDIR

def user_check(username: str, build: str, pod: str, workdir: str, ops: str = '') -> int:
	user = User(name = username)
	if user.load_groups() != 0:
		log.error('[ERROR] user load groups:', username)
		return EGROUPS
	if ops != '' and not user.is_operator:
		log.error('[ERROR] unauth user:', username, 'operation', ops)
		return EOPS
	st = EARGS
	if build != '':
		log.debug(user, 'build:', build)
		st = _check_app(user, "uwsapp_%s" % build)
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
	return st
