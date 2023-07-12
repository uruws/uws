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
	cat testdata/kube/top_nodes.txt
	exit 0

elif test "X${1}" = 'Xtest_top_pods'; then
	cat testdata/kube/top_pods.txt
	exit 0

elif test "X${1}" = 'Xtest_k8s_metrics'; then
	cat testdata/kube/k8s_metrics.txt
	exit 0

elif test "X${1}" = 'Xtest_ngxlogs_error'; then
	echo 'invalid_json'
	exit 0
elif test "X${1}" = 'Xtest_ngxlogs'; then
	echo '{}'
	exit 0

fi
exit 128
