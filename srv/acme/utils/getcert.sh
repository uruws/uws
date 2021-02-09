#!/bin/sh
set -eu

DOM=${1:?'domain?'}

umask 0027
mkdir -vp /srv/run/acme/tmp /srv/acme/cert

AK=/srv/acme/key/account.key
CDIR=/srv/run/acme/challenge/

CSR=/srv/acme/req/${DOM}.csr
CRT=/srv/acme/cert/${DOM}.crt
TMP=/srv/run/acme/tmp/${DOM}.crt

# change umas so the challenge file can be read by the web server
umask 0022

rm -f ${TMP}
acme-tiny --account-key ${AK} --csr ${CSR} --acme-dir ${CDIR} >${TMP} || {
	echo "acme gen ${CRT}: failed!" >&2
	exit 1
}

# restore umask
umask 0027

cat ${TMP} >${CRT}
rm -vf ${TMP}

echo 'true' >/srv/run/acme/tmp/reload
exit 0
