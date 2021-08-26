#!/bin/sh
set -eu
uwskube create secret generic uwsca-ops \
	--from-file=ca.crt=${HOME}/ca/uws/ops/210823/rootCA.pem \
	--from-file=ca.crl=${HOME}/ca/uws/ops/210823/rootCA-crl.pem
~/k8s/gateway/deploy.sh
exit 0
