#!/bin/sh
set -eu
DOM=${1:?'domain?'}

umask 0027
mkdir -vp /srv/acme/req

umask 0077

KN=/srv/acme/key/${DOM}.key
if test ! -s ${KN}; then
	echo "${KN}: file not found, aborting!" >&2
	exit 2
fi

FN=/srv/acme/req/${DOM}.csr
if test -s ${FN}; then
	echo "${FN}: file already exists, aborting!" >&2
	exit 3
fi

SUBJ="/CN=${DOM}"
ARGS=''
if test $# -gt 1; then
	SUBJ="/"
	ID=1
	for dom in $(echo $@); do
		ARGS="${ARGS} DNS:${dom},"
	done
	ARGS=$(echo ${ARGS} | sed 's/,$//')
fi

if test "X${ARGS}" = 'X'; then
	echo "SUBJ: ${SUBJ}"
	openssl req -new -sha256 -key ${KN} -subj ${SUBJ} >${FN}
else
	echo "SUBJ: ${ARGS}"
	openssl req -new -sha256 -key ${KN} -subj ${SUBJ} -addext "subjectAltName=${ARGS}" >${FN}
fi

echo "${FN}: done!"
exit 0
