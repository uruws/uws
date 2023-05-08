#!/bin/sh
set -eu

action=${1:?'action?'}
shift

if ! test -x "${action}"; then
	echo "invalid action: ${action}" >&2
	exit 3
fi

for ef in eks/env/*.env; do
	cluster=$(basename "${ef}" .env)
	echo '***'
	echo "*** ${cluster}"
	echo '***'
	./eks/cmd.sh "${cluster}" "${action}" $@
done

exit 0
