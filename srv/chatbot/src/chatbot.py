# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging
import shlex

from dataclasses import dataclass
from os          import getenv
from pathlib     import Path
from subprocess  import getstatusoutput
from typing      import Optional

#
# config
#

debug:         bool = getenv('UWS_WEBAPP_DEBUG', 'off') == 'on'
libexec:       Path = Path('/opt/uws/chatbot/libexec')
uwscli_cmd:    str  = 'uwscli.sh'
uwscli_host:   str  = getenv('UWSCLI_HOST', 'localhost')
uwscli_bindir: str  = Path('/srv/home/uwscli/bin')
webapp_port:   int  = int(getenv('UWS_WEBAPP_PORT', '2741'))

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
# utils
#

@dataclass
class UwscliCmd(object):
	enable: bool

uwscli_command: dict[str, UwscliCmd] = {
	'app-build': UwscliCmd(
		enable = True,
	),
	'app-deploy': UwscliCmd(
		enable = True,
	),
	'app-events': UwscliCmd(
		enable = True,
	),
	'app-logs': UwscliCmd(
		enable = True,
	),
	'app-restart': UwscliCmd(
		enable = True,
	),
	'app-rollin': UwscliCmd(
		enable = True,
	),
	'app-scale': UwscliCmd(
		enable = True,
	),
	'app-status': UwscliCmd(
		enable = True,
	),
	'app-top': UwscliCmd(
		enable = True,
	),
	'production-tapo': UwscliCmd(
		enable = True,
	),
	'staging-tapo': UwscliCmd(
		enable = True,
	),
	'uwshelp': UwscliCmd(
		enable = True,
	),
}

def uwscli(user: str, cmd: str) -> tuple[int, str]:
	logging.debug('uwscli: %s %s', user, cmd)
	# user
	u = user_get(user)
	if u is None:
		logging.error('uwscli invalid user: %s', user)
		return (-1, 'unauthorized')
	# command
	xcmd = f"{libexec}/{uwscli_cmd} {uwscli_host} {u.name}"
	icmd = cmd.split()
	xn = icmd[0].strip()
	x = uwscli_command.get(xn, None)
	if x is None:
		logging.error('uwscli invalid command: %s', xn)
		return (-2, 'unauthorized')
	if not x.enable:
		logging.error('uwscli disabled command: %s', xn)
		return (-3, 'unauthorized')
	xcmd += ' %s' % uwscli_bindir.joinpath(xn)
	for a in icmd[1:]:
		xcmd += ' %s' % shlex.quote(a)
	# exec
	logging.debug('uwscli exec: %s', xcmd)
	return getstatusoutput(xcmd)
