#!/bin/sh
set -eu
uwskube create secret tls tapo-wild-certificate \
	--cert=${HOME}/ca/godaddyCerts/bundled_all.crt \
	--key=${HOME}/ca/godaddyCerts/server.key

envsubst <${HOME}/cluster/web-gateway.yaml | uwskube apply -f -
exit 0
