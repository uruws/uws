#!/bin/sh
set -eu

action=${1:?'action?'}

deploy() {
	local cluster="${1}"
	./docker/k8s/cli.sh "${cluster}" ./k8s/mon/deploy.sh
}

status() {
	local cluster="${1}"
	./docker/k8s/cli.sh "${cluster}" ./k8s/mon/status.sh
}

munin_node_restart() {
	local cluster="${1}"
	./docker/k8s/cli.sh "${cluster}" ./k8s/mon/munin-node/restart.sh
}

for ef in $(ls ./eks/env/*.env); do
	cluster=$(basename ${ef} .env)
	echo "*** ${cluster}"
	if test "X${action}" = 'Xdeploy'; then
		deploy ${cluster}
	elif test "X${action}" = 'Xstatus'; then
		status ${cluster}
	elif test "X${action}" = 'Xmunin-node/restart'; then
		munin_node_restart ${cluster}
	else
		echo "invalid action: ${action}" >&2
		exit 3
	fi
done

exit 0
