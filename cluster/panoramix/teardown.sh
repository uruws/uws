#!/bin/sh
set -eu
cluster=/home/uws/cluster/panoramix
uwskube delete -f ${cluster}/gateway.yaml
exit 0
