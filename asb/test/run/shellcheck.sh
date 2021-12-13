#!/bin/sh
set -eu
find ${HOME}/asb ${HOME}/ca ${HOME}/secret -type f -name '*.sh' -print0 |
	xargs --null -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning
exit 0
