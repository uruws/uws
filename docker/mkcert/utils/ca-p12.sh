#!/bin/sh
set -eu

FN=${1:?'cert file name?'}
NAME=${2:?'cert friendly name?'}

CAFN="${HOME}/ca/rootCA.pem"
P12FN="${HOME}/ca/client/${FN}.p12"
CRTFN="${HOME}/ca/client/${FN}.pem"
KEYFN="${HOME}/ca/client/${FN}-key.pem"

umask 0027

getpw() {
	fn="${1}"
	pw=$(grep -F "${fn}:" /usr/local/etc/ca/client.pw | cut -d ':' -f 2)
	if test 'X' = "X${pw}"; then
		echo "ERROR - ${fn}: no password found!" >&2
		echo ""
	fi
	echo "${pw}"
}

P12PW=$(getpw ${FN})
if test 'X' = "X${P12PW}"; then
	P12PW="changeit"
fi

tmp_p12=$(mktemp -t p12.XXXXXXXX)
mv -f "${P12FN}" "${tmp_p12}"

# stolen from: https://gist.github.com/slabko/5c3210207b2c2d62a61148389fc94800

openssl pkcs12 -in ${tmp_p12} -passin pass:changeit -nocerts \
	-out ${KEYFN} -passout pass:${P12PW}

openssl pkcs12 -in ${tmp_p12} -passin pass:changeit -clcerts -nokeys \
	-out ${CRTFN}

openssl pkcs12 -export -name "${NAME}" \
	-in ${CRTFN} -inkey ${KEYFN} \
	-passin pass:${P12PW} \
	-out ${P12FN} -passout pass:${P12PW} \
	-no-CAfile -no-CApath \
	-certfile ${CAFN}

rm -f ${tmp_p12}

export OPENSSL_CONF=/usr/local/etc/ssl/openssl.cnf
exec openssl ca -valid "${CRTFN}"
