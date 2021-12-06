#!/bin/sh
set -eu
uwskube create secret tls tapo-wild-certificate \
	--cert=${HOME}/ca/godaddyCerts/bundled_all.crt \
	--key=${HOME}/ca/godaddyCerts/server.key

uwskube apply -f ~/cluster/web-gateway.yaml
exit 0
