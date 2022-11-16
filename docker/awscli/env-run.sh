#!/bin/sh
set -eu

envname=${1:?'env name?'}
CMD=${2:?'command?'}

cd "$(dirname $0)"/../../

awsdir=${PWD}/secret/aws.env/${envname}
if ! test -d ${awsdir}; then
	echo "${awsdir}: env not found" >&2
	exit 1
fi

awsdir=${PWD}/secret/aws
utils=${PWD}/docker/awscli/utils

docker run --rm --name uws-awscli-env-${envname} \
	--hostname awscli-env-${envname}.uws.local \
	-u uws \
	--entrypoint "/home/uws/bin/${CMD}" \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${utils}:/home/uws/bin:ro \
	uws/awscli-2211

exit 0
