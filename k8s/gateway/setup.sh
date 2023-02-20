#!/bin/sh
set -eu
uwskube apply -f ${HOME}/k8s/gateway/services.yaml
exec ~/k8s/gateway/deploy.sh
