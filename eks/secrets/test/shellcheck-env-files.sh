#!/bin/sh
set -eu

# SC2034: UWS_WEBAPP_DEBUG appears unused. Verify use (or export if used externally).
# SC2016: Expressions don't expand in single quotes, use double quotes for that.

find ./secret -type f -name '*.env' -print0 |
	xargs --null -- shellcheck --color=auto --shell=sh --severity=error --exclude=SC2034,SC2016

exit 0
