#!/bin/sh
set -eu
count=${1:-"60"}
(timeout ${count} ./k8s/nginx-ingress/logs.sh -f | wc -l)
exit 0
