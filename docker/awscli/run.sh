#!/bin/sh
set -eu

CMD=${1:?'command?'}

awsdir=${PWD}/secret/aws
utils=${PWD}/docker/awscli/utils

docker run --rm --name uws-awscli --hostname awscli.uws.local \
	-u uws \
	--entrypoint "${CMD}" \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${utils}:/home/uws/bin:ro \
	uws/awscli-2203

exit 0
