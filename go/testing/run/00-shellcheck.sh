#!/bin/sh
set -eu
find /go/src/uws -type f -name '*.sh' -print0 | xargs --null -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning
exit 0
