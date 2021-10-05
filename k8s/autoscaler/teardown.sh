#!/bin/sh
set -u
exec uwskube delete -f ~/k8s/autoscaler/deploy.yaml
