#!/bin/sh
set -eu

cluster=/home/uws/cluster/amybeta

uwskube create secret generic basic-auth --from-file=auth=${HOME}/secret/auth
uwskube get secret basic-auth -o yaml

uwskube apply -f ${cluster}/gateway.yaml

exit 0
