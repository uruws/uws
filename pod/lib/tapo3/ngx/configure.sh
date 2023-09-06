#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}

srcf=${HOME}/pod/tapo3/${app}/nginx.conf

gw=$(mktemp -d -p /tmp "nginx-${app}-configure.XXXXXXXXXX")

install -v -d -m 0755 "${gw}/sites-enabled"

<"${srcf}" envsubst '${METEOR_NAMESPACE}' |
	envsubst '${TAPO_API_NAMESPACE}' |
	envsubst '${METEOR_TLS}' |
	envsubst '${METEOR_HOST}' >"${gw}/sites-enabled/tapo3-${app}"

# sites-enabled
uwskube delete secret "sites-${app}-enabled" -n "${ns}" || true
uwskube create secret generic "sites-${app}-enabled" -n "${ns}" \
	--from-file="${gw}/sites-enabled"

rm -rf "${gw}"
exit 0
