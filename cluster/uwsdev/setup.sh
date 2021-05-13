#!/bin/sh
set -eu

. ~/bin/env.export

cluster=~/cluster/${UWS_CLUSTER}

set -x

uwskube apply -f ~/k8s/acme/staging.yaml

uwskube create secret generic basic-auth --from-file=auth=~/secret/auth
uwskube get secret basic-auth -o yaml

uwskube apply -f ~/cluster/${cluster}/gateway.yaml

exit 0
