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

exec docker run -it --rm --read-only \
	--name "uws-${webapp}-devel" \
	--hostname "${webapp}-devel.uws.local" \
	--entrypoint /usr/local/bin/devel-entrypoint.sh \
	--env-file "${webapp_env}" \
	-v "${tmpdir}:/home/uws/tmp" \
	-v "${PWD}/docker/webapp/utils:/usr/local/bin:ro" \
	-v "${webapp_src}:/opt/uws/${webapp}:ro" \
	--workdir /home/uws \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	"uws/${webapp}-2211"
