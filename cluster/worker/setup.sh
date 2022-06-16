#!/bin/sh
set -eu

~/k8s/gateway/setup.sh
~/k8s/mon/setup.sh

uwskube create secret tls tapo-wild-certificate \
	--cert=${HOME}/ca/godaddyCerts/bundled_all.crt \
	--key=${HOME}/ca/godaddyCerts/server.key

exit 0
