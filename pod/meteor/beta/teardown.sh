#!/bin/sh
set -eu
uwskube delete secret -n meteor-beta meteor-beta-env || true
uwskube delete namespace meteor-beta
uwskube delete -f ~/cluster/meteor-gateway.yaml
exit 0
