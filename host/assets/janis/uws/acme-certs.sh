#!/bin/sh
set -eu

export ACME_HOME=/srv/acme
export ACME_RUN=/srv/run/acme

acme=/srv/uws/deploy/srv/acme/cmd.sh
list=/uws/acme-certs.list

for cn in $(cat ${list} | cut -d ' ' -f 1); do
	keyfn=${ACME_HOME}/key/${cn}.key
	echo "i - ${keyfn}"
	if ! test -s ${keyfn}; then
		${acme} keygen.sh ${cn}
	fi
done

echo 'false' >/srv/run/acme/tmp/reload

cat ${list} | while read line; do
	cn=$(echo "${line}" | cut -d ' ' -f 1)
	reqfn=${ACME_HOME}/req/${cn}.csr
	echo "i - req ${line}"
	if ! test -s ${reqfn}; then
		${acme} reqnew.sh ${line}
	fi
	echo "i - crt ${cn}"
	${acme} getcert.sh ${cn}
done

exit 0
