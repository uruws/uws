#!/bin/sh
set -eu

. ~/bin/env.export

cluster=~/cluster/${UWS_CLUSTER}

set -x

uwskube apply -f ~/k8s/acme-staging.yaml
uwskube apply -f ${cluster}/certificates.yaml

uwskube create secret generic basic-auth --from-file=auth=~/secret/auth
uwskube get secret basic-auth -o yaml

exit 0
