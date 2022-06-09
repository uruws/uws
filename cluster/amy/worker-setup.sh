#!/bin/sh
set -eu

#~ uwskube create secret tls tapo-wild-certificate \
	#~ --cert=${HOME}/ca/godaddyCerts/bundled_all.crt \
	#~ --key=${HOME}/ca/godaddyCerts/server.key

exec uwskube apply -f ~/cluster/worker-gateway.yaml
