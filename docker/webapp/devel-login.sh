#!/bin/sh
set -eu

tmpdir="${PWD}/tmp/webapp"
install -v -d -m 0750 "${tmpdir}"

exec docker run -it --rm --read-only \
	--name uws-webapp-devel \
	--hostname webapp-devel.uws.local \
	-p 127.0.0.1:0:2741 \
	-v "${PWD}/docker/webapp/utils:/opt/webapp/utils:ro" \
	-v "${PWD}/docker/webapp/utils.test:/opt/uws/test:ro" \
	-v "${PWD}/docker/webapp/src:/opt/uws/lib:ro" \
	-v "${tmpdir}:/home/uws/tmp" \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	-e UWS_WEBAPP=devel \
	--tmpfs /tmp \
	--workdir /home/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	"uws/webapp-2305"
