#!/bin/sh
set -u

export ACME_HOME=/srv/acme
export ACME_RUN=/srv/run/acme

acme=/srv/uws/deploy/srv/acme/cmd.sh
list=/uws/acme-certs.list

if ! test -r ${list}; then
	echo "ERROR: ${list} file not found" >&2
	exit 1
fi

cksum=$(md5sum ${list} | cut -d ' ' -f 1)
flag=/srv/run/acme/tmp/done-${cksum}.$(date '+%Y%m')
if test -s ${flag}; then
	echo "i - ${flag} found, not running again."
	exit 0
fi
rm -vf /srv/run/acme/tmp/done.*

for cn in $(cat ${list} | cut -d ' ' -f 1); do
	keyfn=${ACME_HOME}/key/${cn}.key
	if ! test -s ${keyfn}; then
		echo "i - keygen ${keyfn}"
		${acme} keygen.sh ${cn}
	fi
done

echo 'false' >/srv/run/acme/tmp/reload

cat ${list} | while read line; do
	cn=$(echo "${line}" | cut -d ' ' -f 1)
	reqfn=${ACME_HOME}/req/${cn}.csr
	if ! test -s ${reqfn}; then
		echo "i - reqnew ${line}"
		${acme} reqnew.sh ${line}
	fi
	echo "i - getcert ${cn}"
	${acme} getcert.sh ${cn}
done

echo 1 >${flag}
exit 0
