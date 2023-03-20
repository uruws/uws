#!/bin/sh
set -eu

find ${HOME}/bin ${HOME}/cluster ${HOME}/eks \
	-type f -name '*.sh' -print0 |
	xargs --null -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning \
		--exclude=SC1071

# SC1071: ShellCheck only supports sh/bash/dash/ksh scripts. Sorry!

exit 0
