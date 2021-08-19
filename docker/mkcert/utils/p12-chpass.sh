#!/bin/sh
set -eu

CAFN=${1:?'CA file?'}
INFN=${2:?'input file?'}
OUTFN=${3:?'output file?'}

umask 0027

tmp_crt=$(mktemp -t p12-crt.XXXXXXXX)
tmp_key=$(mktemp -t p12-key.XXXXXXXX)

# stolen from: https://gist.github.com/slabko/5c3210207b2c2d62a61148389fc94800

openssl pkcs12 -in ${INFN} -passin pass:changeit -nocerts \
	-out ${tmp_key} -passout pass:changeit

openssl pkcs12 -in ${INFN} -passin pass:changeit -clcerts -nokeys \
	-out ${tmp_crt}

openssl pkcs12 -export \
	-in ${tmp_crt} -inkey ${tmp_key} \
	-passin pass:changeit \
	-out ${OUTFN} -passout pass:${P12PW} \
	-chain -CAfile ${CAFN} -no-CApath

rm -f ${tmp_crt} ${tmp_key}
echo "${OUTFN} created!"

exit 0
