#!/bin/sh
set -eu
uwskube delete -f ~/k8s/ca/deploy.yaml
exit 0
