#!/bin/sh
set -eu
ca=opstest/220414
uwskube create secret generic uwsca-opstest \
	--from-file=ca.crt=${HOME}/ca/uws/${ca}/rootCA.pem \
	--from-file=ca.crl=${HOME}/ca/uws/${ca}/rootCA-crl.pem
exit 0
