#!/bin/sh
set -u
~/k8s/gateway/rollin.sh
uwskube delete -f ${HOME}/k8s/gateway/services.yaml
exit 0
