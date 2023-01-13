#!/bin/sh
set -u
exec uwskube delete -f ${HOME}/k8s/autoscaler/${K8S_VERSION}/deploy.yaml
