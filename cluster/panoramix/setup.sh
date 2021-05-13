#!/bin/sh
set -eu
cluster=/home/uws/cluster/panoramix
uwskube apply -f ${cluster}/gateway.yaml
exit 0
