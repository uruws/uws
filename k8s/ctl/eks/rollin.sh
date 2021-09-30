#!/bin/sh
set -u
uwskube delete cronjob eks-nodegroup-upgrade -n ctl
uwskube delete jobs -n ctl --all
#~ uwskube delete secret aws-auth -n ctl
uwskube delete secret cluster-auth -n ctl
uwskube delete configmap cluster-env -n ctl
exit 0
