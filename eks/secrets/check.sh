#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp
install -v -d -m 0750 "${TMPDIR}"

exec docker run --rm --name uws-secrets-check \
	--hostname secrets-check.ansible.uws.local -u uws \
	--read-only \
	-v "${TMPDIR}:/home/uws/tmp" \
	-v "${PWD}/eks/secrets:/home/uws/eks/secrets:ro" \
	-v "${PWD}/secret:/home/uws/secret:ro" \
	--workdir /home/uws \
	uws/python-2309 ./eks/secrets/test/run.sh
