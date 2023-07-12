#!/bin/sh
set -eu
ln -sf "/home/uws/.kube/eksctl/clusters/${UWS_CLUSTER}" /home/uws/.kube/config
exec /usr/local/bin/kubeshark "$@"
