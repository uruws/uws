#!/bin/sh
set -eu
uwskube apply -f ~/k8s/mon/munin-web/deploy.yaml
exit 0
