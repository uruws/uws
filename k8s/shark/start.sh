#!/bin/sh
set -eu
cluster=${UWS_CLUSTER}
ln -sf "/home/uws/.kube/eksctl/clusters/${cluster}" /home/uws/.kube/config
exec kubeshark "$@"
