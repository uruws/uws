# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging
import shlex

from os         import getenv
from pathlib    import Path
from subprocess import getstatusoutput

#
# config
#

debug:       bool = getenv('UWS_WEBAPP_DEBUG', 'off') == 'on'
libexec:     Path = Path('/opt/uws/chatbot/libexec')
uwscli_cmd:  str  = 'uwscli.sh'
uwscli_host: str  = getenv('UWSCLI_HOST', 'localhost')
webapp_port: int  = int(getenv('UWS_WEBAPP_PORT', '2741'))

#
# utils
#

def uwscli(user: str, cmd: str) -> tuple[int, str]:
	logging.debug('uwscli: %s %s', user, cmd)
	xcmd = f"{libexec}/{uwscli_cmd} {uwscli_host} {user}"
	for a in cmd.split():
		xcmd += ' %s' % shlex.quote(a)
	logging.debug('uwscli exec: %s', xcmd)
	return getstatusoutput(xcmd)
