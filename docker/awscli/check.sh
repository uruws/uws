#!/bin/sh
set -eu

utils=${PWD}/docker/awscli/utils
testd=${PWD}/docker/awscli/test

tmpdir=${PWD}/tmp/awscli
install -v -d -m 0750 ${tmpdir}

exec docker run --rm --name uws-awscli-check \
	--hostname awscli-check.uws.local \
	--read-only \
	--workdir /home/uws \
	-v ${utils}:/home/uws/bin:ro \
	-v ${testd}:/home/uws/test:ro \
	-v ${tmpdir}:/home/uws/tmp \
	uws/python-2309 /home/uws/test/check.sh
