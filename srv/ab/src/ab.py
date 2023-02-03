# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os          import getenv
from pathlib     import Path

#
# config
#

debug:       bool = getenv('UWS_WEBAPP_DEBUG', 'off') == 'on'
webapp_port: int  = int(getenv('UWS_WEBAPP_PORT', '2741'))
