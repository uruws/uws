#!/bin/sh
set -eu

webapp=${1:?'webapp name?'}
shift

webapp_src="${PWD}/srv/${webapp}/src"
webapp_env="${PWD}/secret/webapp/${webapp}.env"
webapp_confd="${PWD}/secret/webapp/${webapp}"

if ! test -d "${webapp_src}"; then
	echo "${webapp}: invalid webapp" >&2
	exit 9
fi

if ! test -d "${webapp_confd}"; then
	echo "${webapp_confd}: webapp conf dir not found" >&2
	exit 9
fi

tmpdir="${PWD}/tmp/${webapp}"
install -v -d -m 0750 "${tmpdir}"

exec docker run --rm --read-only \
	--name "uws-${webapp}-cmd" \
	--hostname "${webapp}-cmd.uws.local" \
	--env-file "${webapp_env}" \
	-v "${webapp_confd}:/etc/opt/uws/${webapp}:ro" \
	-v "${tmpdir}:/home/uws/tmp" \
	--workdir "/opt/uws/${webapp}" \
	--entrypoint /usr/local/bin/webapp-check.sh \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--tmpfs /tmp \
	"uws/${webapp}-2211" "$@"
