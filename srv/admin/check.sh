#!/bin/sh
set -eu

webapp=admin

webapp_src="${PWD}/srv/${webapp}/src"
webapp_env="${PWD}/secret/webapp/devel/${webapp}.env"
webapp_confd="${PWD}/secret/webapp/devel/${webapp}"

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
	--name "uws-${webapp}-check" \
	--hostname "${webapp}-check.uws.local" \
	--env-file "${webapp_env}" \
	-v "${PWD}/docker/webapp/utils.test:/opt/uws/test:ro" \
	-v "${PWD}/docker/webapp/src/test:/opt/uws/lib/test:ro" \
	-v "${webapp_src}/test:/opt/uws/${webapp}/test:ro" \
	-v "${webapp_confd}:/etc/opt/uws/${webapp}:ro" \
	-v "${tmpdir}:/home/uws/tmp" \
	--workdir "/opt/uws/${webapp}" \
	--entrypoint /usr/local/bin/webapp-check.sh \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--tmpfs /tmp \
	-v "${PWD}/host/assets/jsbatch/srv/home/uwscli/lib:/srv/home/uwscli/lib:ro" \
	uws/admin-2305 "$@"
