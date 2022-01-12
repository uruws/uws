#!/bin/sh
set -eu
uwskube create namespace meteor-beta
uwskube apply -f ~/cluster/meteor-gateway.yaml
exit 0
