#!/bin/sh
set -eu
awsdir=${PWD}/secret/aws
docker run --rm --name uws-awscli-cmd --hostname awscli-cmd.uws.local -u uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	uws/awscli-2309 "$@"
exit 0
