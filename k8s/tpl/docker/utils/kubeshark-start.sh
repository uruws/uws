#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
shift
ln -sf "/home/uws/.kube/eksctl/clusters/${cluster}" /home/uws/.kube/config
exec kubeshark "$@"
