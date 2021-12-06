#!/bin/sh
set -eu

find ${HOME}/bin ${HOME}/cluster ${HOME}/eks \
	-type f |
	grep -vF '.yaml' |
	grep -vF '.md' |
	grep -vF '.env' |
	grep -vF 'eks/lib' |
	grep -vF 'secret/ssh' |
	xargs -- \
	shellcheck --check-sourced --color=auto --norc --severity=warning \
		--exclude=SC1071

# SC1071: ShellCheck only supports sh/bash/dash/ksh scripts. Sorry!

exit 0
