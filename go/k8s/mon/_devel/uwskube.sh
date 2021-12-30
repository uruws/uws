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
elif test "X${1}" = 'Xtest_deployments'; then
	echo '{}'
	exit 0
elif test "X${1}" = 'Xtest_nodes_error'; then
	echo 'invalid_json'
	exit 0
elif test "X${1}" = 'Xtest_nodes'; then
	echo '{}'
	exit 0
elif test "X${1}" = 'Xtest_pods_error'; then
	echo 'invalid_json'
	exit 0
elif test "X${1}" = 'Xtest_pods'; then
	echo '{}'
	exit 0
elif test "X${1}" = 'Xtest_top_nodes'; then
	echo 'ip-192-168-14-101.ec2.internal   62m   3%    731Mi   10%   '
	echo 'ip-192-168-6-89.ec2.internal     63m   3%    887Mi   12%   '
	echo 'ip-192-168-60-59.ec2.internal    73m   3%    891Mi   12%   '
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
