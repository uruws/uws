#!/bin/sh
set -eu

munin_confd=${HOME}/k8s/mon/munin/conf.d
uwskube delete configmap munin-confd -n mon || true
uwskube create configmap munin-confd -n mon \
	--from-file="${munin_confd}"

export VERSION="$(cat ~/k8s/mon/VERSION)"
envsubst <~/k8s/mon/munin/deploy.yaml | uwskube apply -f -

exit 0
