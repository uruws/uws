#!/bin/sh
set -eu
cluster=/home/uws/cluster/panoramix
uwskube delete secret basic-auth
uwskube delete -f ${cluster}/gateway.yaml
exit 0
