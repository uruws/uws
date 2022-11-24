#!/bin/sh
set -eu

profile=${1:?'profile?'}

helm uninstall --wait \
	--namespace "ingress-${profile}" \
	"${profile}"

exec uwskube delete namespace "ingress-${profile}"
