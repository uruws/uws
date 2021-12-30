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

elif test "X${1}" = 'Xtest_top_pods'; then
	echo 'cert-manager    cert-manager-66b6d6bf59-xsx76               1m    23Mi   '
	echo 'cert-manager    cert-manager-cainjector-856d4df858-csjg7    3m    51Mi   '
	echo 'cert-manager    cert-manager-webhook-6d866ffbc7-pq4mw       2m    14Mi   '
	echo 'ingress-nginx   ingress-nginx-controller-59c8576d75-qbms9   3m    76Mi   '
	echo 'kube-system     aws-node-5lmld                              4m    41Mi   '
	echo 'kube-system     aws-node-fp6c6                              5m    41Mi   '
	echo 'kube-system     aws-node-lnmz9                              5m    41Mi   '
	echo 'kube-system     cluster-autoscaler-848d4b88dc-rlvx6         2m    45Mi   '
	echo 'kube-system     coredns-7d74b564bd-9mc2d                    4m    8Mi    '
	echo 'kube-system     coredns-7d74b564bd-l8c2t                    3m    8Mi    '
	echo 'kube-system     kube-proxy-6zggk                            1m    13Mi   '
	echo 'kube-system     kube-proxy-f4jnk                            2m    13Mi   '
	echo 'kube-system     kube-proxy-q2rpf                            1m    13Mi   '
	echo 'kube-system     metrics-server-588cd8ddb5-r6hrq             4m    20Mi   '
	echo 'mon             k8s-54cf879cf8-6k2kv                        1m    15Mi   '
	echo 'mon             munin-0                                     1m    55Mi   '
	echo 'mon             munin-node-789b7d89bf-r97hf                 1m    11Mi   '
	exit 0

fi
exit 128
