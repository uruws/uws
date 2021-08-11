#!/bin/sh
set -eu
uwskube apply -f ~/k8s/mon/munin/deploy.yaml
exit 0
