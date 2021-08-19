#!/bin/sh
set -eu
EMAIL=${1:-'user email?'}
umask 0027
getpw() {
	local fn="${1}"
	local pw=$(grep -F "${fn}:" "${HOME}/ca/client.pw" | cut -d ':' -f 2)
	if test 'X' = "X${pw}"; then
		echo "ERROR - ${fn}: no password found!" >&2
		echo ""
	fi
	echo "${pw}"
}
fn=$(uuidgen --sha1 --namespace '@dns' --name "${EMAIL}")
p12fn="${HOME}/ca/client/${fn}.p12"
mkcert -client -ecdsa -pkcs12 --p12-file "/tmp/${fn}.p12" "$@"

export P12PW=$(getpw ${fn})
if test 'X' = "X${P12PW}"; then
	exit 1
fi
p12-chpass.sh "${HOME}/ca/rootCA.pem" "/tmp/${fn}.p12" "${p12fn}"

rm -f "/tmp/${fn}.p12"
exit 0
