#!/bin/sh
set -eu

profile=${1:?'profile?'}

helm uninstall --wait \
	--namespace "ingress-${profile}" \
	"nginx-${profile}"

exec uwskube delete namespace "ingress-${profile}"
