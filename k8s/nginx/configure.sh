#!/bin/sh
set -eu

ns=${1:?'namespace?'}
gw=${2:?'gateway?'}

#~ # nginx.env
#~ uwskube delete secret proxy-env -n "${ns}" || true
#~ uwskube create secret generic proxy-env -n "${ns}" \
	#~ --from-env-file=${gw}/nginx.env

# sites-enabled
uwskube delete secret sites-enabled -n "${ns}" || true
uwskube create secret generic sites-enabled -n "${ns}" \
	--from-file="${gw}/nginx/sites-enabled"

# godaddy certs
~/ca/godaddyCerts/setup.sh "${ns}"

# internal CA
~/k8s/ca/uws/ops/setup.sh "${ns}"

exit 0
