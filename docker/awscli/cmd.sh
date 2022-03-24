#!/bin/sh
set -eu
awsdir=${PWD}/secret/aws
utils=${PWD}/docker/awscli/utils
docker run --rm --name uws-awscli-cmd --hostname awscli-cmd.uws.local -u uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws \
	-v ${utils}:/home/uws/bin \
	uws/awscli-2203 "$@"
exit 0
