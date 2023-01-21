# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import logging

from pathlib    import Path
from subprocess import getstatusoutput

libexec     = Path('/opt/uws/chatbot/libexec')
uwscli_cmd  = 'uwscli.sh'
uwscli_host = 'localhost'

def uwscli(user: str, cmd: str) -> tuple[int, str]:
	logging.debug('uwscli: %s %s', user, cmd)
	xcmd = f"{libexec}/{uwscli_cmd} {uwscli_host} {user} {cmd}"
	logging.debug('uwscli exec: %s', xcmd)
	return getstatusoutput(xcmd)
