#!/bin/sh
set -eu
find /srv/uws/deploy/cli -type f -name '*.sh' |
	xargs shellcheck --check-sourced --color=auto --norc --shell=sh --severity=warning
exit 0
