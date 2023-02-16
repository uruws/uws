#!/bin/sh
set -eu
uwskube logs -n kube-system \
	-l "app.kubernetes.io/name=aws-efs-csi-driver,app.kubernetes.io/instance=aws-efs-csi-driver" \
	"$@"
