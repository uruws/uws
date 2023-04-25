#!/bin/sh
set -eu
helm repo add haproxy https://haproxy-ingress.github.io/charts
helm repo update
helm search repo haproxy -l | sort -V -k2
exit 0
