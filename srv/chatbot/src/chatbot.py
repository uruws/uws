# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import shlex

from dataclasses import dataclass
from dataclasses import field
from os          import getenv
from pathlib     import Path
from subprocess  import getstatusoutput
from typing      import Optional

import wapp

log = wapp.getLogger(__name__)

#
# config
#

libexec: Path = Path('/opt/uws/chatbot/libexec')

#
# users
#

@dataclass
class User(object):
	name:     str
	slack_id: str = ''

user: dict[str, User] = {}

def user_get(uid: str) -> Optional[User]:
	u = user.get(uid, None)
	if u is not None:
		u.slack_id = uid
	return u

#
# uwscli
#

uwscli_cmd:    str  = 'uwscli.sh'
uwscli_host:   str  = getenv('UWSCLI_HOST', 'localhost')
uwscli_bindir: Path = Path('/srv/home/uwscli/bin')

@dataclass
class UwscliCmdStatus(Exception):
	command: str
	status:  int = -999
	output:  str = ''

@dataclass
class UwscliCmdError(Exception):
	status:  int
	message: str

@dataclass
class UwscliCmd(object):
	enable: bool
	args:   list[str] = field(default_factory = list)

uwscli_command: dict[str, UwscliCmd] = {}

def _uwscli_check(cmd):
	failed = 0
	if cmd.find('|') >= 0:
		failed = 10
	if cmd.find(';') >= 0:
		failed = 11
	if failed > 0:
		raise UwscliCmdError(failed, 'invalid command')

def uwscli(user: str, cmd: str) -> UwscliCmdStatus:
	log.debug('uwscli: %s %s', user, cmd)
	_uwscli_check(cmd)
	proc = UwscliCmdStatus(cmd)
	# user
	u = user_get(user)
	if u is None:
		log.error('uwscli invalid user: %s', user)
		proc.status = -1
		proc.output = 'unauthorized: %s' % user
		return proc
	# command
	xcmd = f"{libexec}/{uwscli_cmd} {uwscli_host} {u.name}"
	icmd = shlex.split(cmd)
	xn = shlex.quote(icmd[0].strip())
	x = uwscli_command.get(xn, None)
	if x is None:
		log.error('uwscli invalid command: %s', xn)
		raise UwscliCmdError(1, 'unauthorized')
	if not x.enable:
		log.error('uwscli disabled command: %s', xn)
		raise UwscliCmdError(2, 'unauthorized')
	xcmd += ' %s' % uwscli_bindir.joinpath(xn)
	# args (config)
	if len(x.args) > 0:
		for a in x.args:
			xcmd += ' %s' % shlex.quote(a)
	# args (user)
	for a in icmd[1:]:
		xcmd += ' %s' % shlex.quote(a)
	# exec
	log.debug('uwscli exec: %s', xcmd)
	proc.command = xcmd
	proc.status, proc.output = getstatusoutput(xcmd)
	return proc
