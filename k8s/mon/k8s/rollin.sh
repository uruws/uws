#!/bin/sh
set -u
uwskube delete secret aws-auth -n mon
uwskube delete secret cluster-auth -n mon
uwskube delete configmap cluster-env -n mon
uwskube delete deploy k8s -n mon
exit 0
