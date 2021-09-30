#!/bin/sh
set -eu

action=${1:?'action?'}

setup() {
	local cluster="${1}"
	./eks/cmd.sh "${cluster}" ./k8s/ctl/setup.sh
}

teardown() {
	local cluster="${1}"
	./eks/cmd.sh "${cluster}" ./k8s/ctl/teardown.sh || true
}

deploy() {
	local cluster="${1}"
	./eks/cmd.sh "${cluster}" ./k8s/ctl/deploy.sh
}

status() {
	local cluster="${1}"
	./eks/cmd.sh "${cluster}" ./k8s/ctl/status.sh
}

for ef in $(ls ./eks/env/*.env); do
	cluster=$(basename ${ef} .env)
	echo "*** ${cluster}"
	if test "X${action}" = 'Xsetup'; then
		setup ${cluster}
	elif test "X${action}" = 'Xteardown'; then
		teardown ${cluster}
	elif test "X${action}" = 'Xdeploy'; then
		deploy ${cluster}
	elif test "X${action}" = 'Xstatus'; then
		status ${cluster}
	else
		echo "invalid action: ${action}" >&2
		exit 3
	fi
done

exit 0
