#!/bin/sh
set -eux
replicas=${1:?'replicas?'}
web_replicas=$(uwskube get deployment/meteor -n web --output jsonpath='{.spec.replicas}')
gw_replicas=$(expr ${replicas} + ${web_replicas})
~/pod/lib/scale.sh api meteor "${replicas}"
~/pod/meteor/web/gw/scale.sh "${gw_replicas}"
exit 0
