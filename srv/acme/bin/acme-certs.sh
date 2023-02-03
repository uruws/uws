#!/bin/sh
set -u
ACME_HOME=/srv/acme

acme=${ACME_HOME}/bin/acme-cmd.sh
list=${ACME_HOME}/etc/certs.list

if ! test -r ${list}; then
	echo "ERROR: ${list} file not found" >&2
	exit 1
fi

install -v -d -m 0750 ${ACME_HOME}/key ${ACME_HOME}/req

TMPDIR=/srv/acme/run/tmp
install -v -d -m 1777 ${TMPDIR}

cksum=$(md5sum ${list} | cut -d ' ' -f 1)
flag=${TMPDIR}/done-${cksum}.$(date '+%Y%m')
if test -s ${flag}; then
	echo "i - ${flag} found, not running again."
	exit 0
fi
rm -vf ${TMPDIR}/done-*.*

#~ acctfn=${ACME_HOME}/key/account.key
#~ if ! test -s ${acctfn}; then
	#~ echo "i - keygen ${acctfn}"
	#~ ${acme} keygen.sh account
#~ fi

for cn in $(cat ${list} | cut -d ' ' -f 1); do
	keyfn=${ACME_HOME}/key/${cn}.key
	if ! test -s ${keyfn}; then
		echo "i - keygen ${keyfn}"
		${acme} keygen.sh ${cn}
	fi
done

echo 'false' >${TMPDIR}/reload

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
