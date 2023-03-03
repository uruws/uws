#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
api_replicas=$(uwskube get deployment/meteor -n api --output jsonpath='{.spec.replicas}')
gw_replicas=$(expr ${replicas} ${api_replicas})
~/pod/lib/scale.sh web meteor "${replicas}"
~/pod/meteor/web/gw/scale.sh "${gw_replicas}"
exit 0
