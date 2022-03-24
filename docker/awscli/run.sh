#!/bin/sh
set -eu
awsdir=${PWD}/secret/aws
utils=${PWD}/docker/awscli/utils
docker run -it --rm --name uws-awscli --hostname awscli.uws.local -u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws \
	-v ${utils}:/home/uws/bin \
	uws/awscli-2203 -il
exit 0
