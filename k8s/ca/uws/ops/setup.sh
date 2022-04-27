#!/bin/sh
set -eu
ca=ops/210823
uwskube create secret generic uwsca-ops \
	--from-file=ca.crt=${HOME}/ca/uws/${ca}/rootCA.pem \
	--from-file=ca.crl=${HOME}/ca/uws/${ca}/rootCA-crl.pem
exit 0
