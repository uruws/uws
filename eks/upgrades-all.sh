#!/bin/sh
set -eu

eksls() (
	for fn in docker/eks/*/Dockerfile.????; do basename "$(dirname "$fn")"; done | sort -u
)

for eks in $(eksls); do
	./docker/upgrades.py -t "uws/eks-${eks}" -U "docker/eks/${eks}" -s "uws/k8s-${eks}"
	./docker/upgrades.py -t "uws/eks-${eks}"
done

exit 0
