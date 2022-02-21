#!/bin/sh
export UWS_CLUSTER=uwsdev
export UWSKUBE=/go/src/uws/k8s/ctl/_devel/uwskube.sh
exec go run ./cmd/k8sctl
