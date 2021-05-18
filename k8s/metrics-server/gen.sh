#!/bin/sh
set -eu
REF='21aad6a'
#~ echo "# release ${REF}"
#~ echo '---'
#~ uwskube kustomize github.com/kubernetes-sigs/metrics-server.git/manifests/release?ref=${REF}
echo "# autoscale ${REF}"
echo '---'
uwskube kustomize github.com/kubernetes-sigs/metrics-server.git/manifests/autoscale?ref=${REF}
exit 0
