#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}

tmpdir=$(mktemp -d -p /tmp "ingress-${app}-deploy.XXXXXXXXXX")

ing_head=${HOME}/pod/lib/tapo3/ngx/ingress-head.yaml

<"${ing_head}" envsubst '${METEOR_NAMESPACE}' |
	envsubst '${METEOR_APP}' >"${tmpdir}/ingress.yaml"

ing_spec=${HOME}/pod/tapo3/${app}/ingress-spec.yaml

<"${ing_spec}" envsubst '${METEOR_NAMESPACE}' |
	envsubst '${TAPO_API_NAMESPACE}' |
	envsubst '${METEOR_APP}' |
	envsubst '${METEOR_TLS}' |
	envsubst '${METEOR_HOST}' >>"${tmpdir}/ingress.yaml"

uwskube apply -f "${tmpdir}/ingress.yaml"

rm -rf "${tmpdir}"
exit 0
