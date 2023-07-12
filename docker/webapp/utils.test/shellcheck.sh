#!/bin/sh
set -eu
webapp=${UWS_WEBAPP}
find "/opt/uws/${webapp}" -type f -name '*.sh' -print0 |
	xargs --null -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning
exit 0
