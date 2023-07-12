#!/bin/sh
set -eu

tmpdir="${PWD}/tmp/webapp"
install -v -d -m 0750 "${tmpdir}"

exec docker run --rm --read-only \
	--name "uws-webapp-check" \
	--hostname "webapp-check.uws.local" \
	-v "${PWD}/docker/webapp/utils.test:/opt/uws/test:ro" \
	-v "${PWD}/docker/webapp/src/test:/opt/uws/lib/test:ro" \
	-v "${tmpdir}:/home/uws/tmp" \
	--workdir "/opt/uws/lib" \
	--entrypoint /opt/uws/test/self/check.sh \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--tmpfs /tmp \
	uws/webapp-2305
