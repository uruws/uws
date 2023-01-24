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

debug:       bool = getenv('UWS_WEBAPP_DEBUG', 'off') == 'on'
libexec:     Path = Path('/opt/uws/chatbot/libexec')
uwscli_cmd:  str  = 'uwscli.sh'
uwscli_host: str  = getenv('UWSCLI_HOST', 'localhost')
webapp_port: int  = int(getenv('UWS_WEBAPP_PORT', '2741'))

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

def uwscli(user: str, cmd: str) -> tuple[int, str]:
	logging.debug('uwscli: %s %s', user, cmd)
	u = user_get(user)
	if u is None:
		logging.error('uwscli invalid user: %s', user)
		return (-1, 'unauthorized')
	xcmd = f"{libexec}/{uwscli_cmd} {uwscli_host} {u.name}"
	for a in cmd.split():
		xcmd += ' %s' % shlex.quote(a)
	logging.debug('uwscli exec: %s', xcmd)
	return getstatusoutput(xcmd)
