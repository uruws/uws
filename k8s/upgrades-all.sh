#!/bin/sh
set -eu

k8sls() (
	for fn in docker/k8s/*/Dockerfile.????; do basename $(dirname $fn); done | sort -u
)

for k8s in $(k8sls); do
	./docker/upgrades.py -t "uws/k8s-${k8s}" -U "docker/k8s/${k8s}"
	./docker/upgrades.py -t "uws/k8s-${k8s}"
done

exit 0
