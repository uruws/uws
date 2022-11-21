#!/bin/sh
set -eu

action=${1:?'action?'}

if ! test -x "${action}"; then
	echo "invalid action: ${action}" >&2
	exit 3
fi

export UWSEKSCMD='true'

for ef in eks/env/*.env; do
	cluster=$(basename "${ef}" .env)
	echo '***'
	echo "*** ${cluster}"
	echo '***'
	./docker/eks/admin.sh "${cluster}" "${action}"
done

exit 0
