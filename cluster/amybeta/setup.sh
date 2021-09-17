#!/bin/sh
set -eu
~/k8s/gateway/setup.sh
~/k8s/mon/setup.sh
uwskube apply -f ~/cluster/meteor-gateway.yaml
exit 0
