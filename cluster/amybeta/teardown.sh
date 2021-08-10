#!/bin/sh
set -eu
cluster=/home/uws/cluster/amybeta
uwskube delete -f ${cluster}/meteor-gateway.yaml
exit 0
