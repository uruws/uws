#!/bin/sh
set -eu
awsdir=${PWD}/secret/aws
docker run -it --rm --name uws-awscli --hostname awscli.uws.local -u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws \
	uws/awscli-2203 "$@"
exit 0
