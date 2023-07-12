#!/bin/sh
set -eu
find /opt/uws/lib -type f -name '*.sh' -print0 |
	xargs --null -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning
exit 0
