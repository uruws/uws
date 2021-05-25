#!/bin/sh
set -eu
cluster=/home/uws/cluster/amytest
uwskube create secret generic basic-auth --from-file=auth=${HOME}/secret/auth
uwskube apply -f ${cluster}/gateway.yaml
exit 0
