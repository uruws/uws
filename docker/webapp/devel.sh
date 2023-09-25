#!/bin/sh
set -eu

webapp=${1:?'webapp name?'}
shift

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

webapp_port=${WEBAPP_PORT:-0}

#~ install -v -d -m 1777 "${webapp_src}/__pycache__"
rm -rf "${webapp_src}/__pycache__"

if test -s "${webapp_confd}/ssh/ecdsa_id"; then
	chmod -v 0600 "${webapp_confd}/ssh/ecdsa_id"
fi

action='devel'
if test 'X--exec' = "X${1:-X}"; then
	action='run'
fi

exec docker run -it --rm --read-only \
	--name "uws-${webapp}-${action}" \
	--hostname "${webapp}-${action}.uws.local" \
	--entrypoint /usr/local/bin/devel-entrypoint.sh \
	--env-file "${webapp_env}" \
	-p "127.0.0.1:${webapp_port}:2741" \
	-v "${PWD}/docker/webapp/utils:/usr/local/bin:ro" \
	-v "${PWD}/docker/webapp/utils.test:/opt/uws/test:ro" \
	-v "${PWD}/docker/webapp/src:/opt/uws/lib:ro" \
	-v "${webapp_confd}:/etc/opt/uws/${webapp}:ro" \
	-v "${webapp_src}:/opt/uws/${webapp}" \
	-v "${tmpdir}:/home/uws/tmp" \
	--workdir "/opt/uws/${webapp}" \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	-e "PYTHONPATH=/opt/uws/lib:/etc/opt/uws/${webapp}" \
	--tmpfs /tmp \
	"uws/${webapp}-2309" "$@"
