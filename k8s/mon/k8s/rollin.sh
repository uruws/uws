#!/bin/sh
set -u
uwskube delete secret aws-auth -n mon
uwskube delete secret cluster-auth -n mon
uwskube delete configmap cluster-env -n mon
uwskube delete service k8s -n mon
exec uwskube delete deploy k8s -n mon
