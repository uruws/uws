#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp
install -v -d -m 0750 "${TMPDIR}"

exec docker run -it --rm --name uws-secrets-devel \
	--hostname secrets.ansible.uws.local -u uws \
	--read-only \
	-v "${TMPDIR}:/home/uws/tmp" \
	-v "${PWD}/eks/secrets:/home/uws/eks/secrets:ro" \
	-v "${PWD}/secret:/home/uws/secret:ro" \
	--workdir /home/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	uws/python-2305
