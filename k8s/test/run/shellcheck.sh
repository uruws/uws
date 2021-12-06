#!/bin/sh
set -eu
find ${HOME}/k8s ${HOME}/pod \
	-type f -name '*.sh' -print0 |
	xargs --null -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning
exit 0
