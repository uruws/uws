#!/bin/sh
set -eux

srcd=/srv/mailx/etc
dstd=/etc/opt/mailx

if test -s "${srcd}/ca/rootCA.pem"; then
	install -v -m 0444 "${srcd}/ca/rootCA.pem" "${dstd}/rootCA.pem"
	install -v -m 0444 "${srcd}/ca/rootCA-crl.pem" "${dstd}/rootCA-crl.pem"

	install -v -m 0444 \
		"${srcd}/ca.client/08082dca-8d77-5c81-9a44-94642089b3b1.pem" \
		"${dstd}/08082dca-8d77-5c81-9a44-94642089b3b1.pem"
	install -v -m 0444 \
		"${srcd}/ca.client/08082dca-8d77-5c81-9a44-94642089b3b1.key" \
		"${dstd}/08082dca-8d77-5c81-9a44-94642089b3b1.key"
fi

exit 0
