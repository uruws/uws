#!/bin/sh
export UWS_CLUSTER=uwsdev
export UWSCTL_BINDIR=/go/src/uws/k8s/ctl/_devel/bin
exec go run ./cmd/k8sctl
