#!/bin/sh
set -eu

export ACME_HOME=/srv/acme
export ACME_RUN=/srv/run/acme

acme=/srv/uws/deploy/srv/acme/cmd.sh
list=/uws/acme-certs.list

if ! test -r ${list}; then
	echo "ERROR: ${list} file not found" >&2
	exit 1
fi

# %U	week number of year, with Sunday as first day of week (00..53)
# %Y	year
flag=/srv/run/acme/tmp/done.$(date '+%Y%U')
if test -s ${flag}; then
	echo "i - ${flag} found, not running again."
	exit 0
fi
rm -vf /srv/run/acme/tmp/done.*

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

echo 1 >${flag}
exit 0
