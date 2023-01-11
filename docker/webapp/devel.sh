#!/bin/sh
set -eu

webapp=${1:?'webapp name?'}

webapp_src="${PWD}/srv/${webapp}/src"
webapp_env="${PWD}/secret/webapp/${webapp}.env"

if ! test -d "${webapp_src}"; then
	echo "${webapp}: invalid webapp" >&2
	exit 9
fi

tmpdir="${PWD}/tmp/${webapp}"
install -v -d -m 0750 "${tmpdir}"

webapp_port=${WEBAPP_PORT:-0}

exec docker run -it --rm --read-only \
	--name "uws-${webapp}-devel" \
	--hostname "${webapp}-devel.uws.local" \
	--entrypoint /usr/local/bin/devel-entrypoint.sh \
	--env-file "${webapp_env}" \
	-p "127.0.0.1:${webapp_port}:2741" \
	-v "${tmpdir}:/home/uws/tmp" \
	-v "${PWD}/docker/webapp/utils:/usr/local/bin:ro" \
	-v "${webapp_src}:/opt/uws/${webapp}:ro" \
	--workdir "/opt/uws/${webapp}" \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--tmpfs /tmp \
	"uws/${webapp}-2211"
