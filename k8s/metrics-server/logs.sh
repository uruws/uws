#!/bin/sh
set -eu
exec uwskube logs deploy/metrics-server -n kube-system --tail=1 "$@"
