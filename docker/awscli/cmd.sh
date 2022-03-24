#!/bin/sh
set -eu
awsdir=${PWD}/secret/aws
docker run --rm --name uws-awscli-cmd --hostname awscli-cmd.uws.local -u uws \
	-v ${awsdir}:/home/uws/.aws \
	uws/awscli-2203 "$@"
exit 0
