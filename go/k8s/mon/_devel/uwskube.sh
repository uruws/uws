#!/bin/sh
set -eu

if test "X${1}" = 'Xtesting'; then
	exit 0
elif test "X${1}" = 'Xtest_error_output'; then
	echo 'mock_error' >&2
	exit 1
elif test "X${1}" = 'Xtest_output'; then
	echo 'mock_output'
	exit 0
elif test "X${1}" = 'Xtest_deployments_error'; then
	echo 'invalid_json'
	exit 0
fi

datadir=/go/tmp/k8smon/${UWS_CLUSTER}
fn=${datadir}/NOTSET_IN_DEVEL_UWSKUBE_SH
if test 'Xget nodes -o json' = "X$*"; then
	fn=nodes.json
elif test 'Xget deployments,statefulset,daemonset -A -o json' = "X$*"; then
	fn=deployments.json
elif test 'Xget pods -A -o json' = "X$*"; then
	fn=pods.json
fi
datfn=${datadir}/${fn}

exec cat ${datfn}
