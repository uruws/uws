#!/bin/sh
export UWS_CLUSTER=uwsdev
export UWSKUBE=/go/src/uws/k8s/mon/_devel/uwskube.sh
exec go run ./cmd/k8smon
