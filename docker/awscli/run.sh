#!/bin/sh
set -eu

CMD=${1:?'command?'}

cd "$(dirname $0)"/../../

awsdir=${PWD}/secret/aws
utils=${PWD}/docker/awscli/utils

docker run --rm --name uws-awscli --hostname awscli.uws.local \
	-u uws \
	--entrypoint "/home/uws/bin/${CMD}" \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${utils}:/home/uws/bin:ro \
	uws/awscli-2305

exit 0
