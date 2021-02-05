#!/bin/sh
set -eu

HOST=${1:?'hostname?'}
FQDN=${2:-''}

DOMAIN=${DOMAIN:-'uws.local'}

if test "X${FQDN}" = 'X'; then
	FQDN="${HOST}.${DOMAIN}"
fi

TMP=${PWD}/tmp/host/deploy/${HOST}
rm -rf ${TMP}
mkdir -p ${TMP}

cd ./host && {
	tar -vcf ${TMP}/${HOST}.tar ./all/*.yml ./${HOST}/*.yml
}
echo "${TMP}/${HOST}.tar: done!"

exit 0
