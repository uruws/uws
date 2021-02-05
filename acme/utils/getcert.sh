#!/bin/sh
set -eu

DOM=${1:?'domain?'}

umask 0027
mkdir -vp /srv/acme/tmp /srv/acme/cert

AK=/srv/acme/key/account.key
CDIR=/srv/acme/challenges/

CSR=/srv/acme/req/${DOM}.csr
CRT=/srv/acme/cert/${DOM}.crt
TMP=/srv/acme/tmp/${DOM}.crt

rm -f ${TMP}
acme-tiny --account-key ${AK} --csr ${CSR} --acme-dir ${CDIR} >${TMP} || {
	echo "acme gen ${CRT}: failed!" >&2
	exit 1
}
mv -f ${TMP} ${CRT}

exit 0
