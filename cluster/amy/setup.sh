#!/bin/sh
set -eu
cluster=/home/uws/cluster/amy
uwskube apply -f ${cluster}/gateway.yaml
exit 0
