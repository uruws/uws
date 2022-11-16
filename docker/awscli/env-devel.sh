#!/bin/sh
set -eu
envname=${1:?'env name?'}

awsdir=${PWD}/secret/aws.env/${envname}
if ! test -d ${awsdir}; then
	echo "${awsdir}: env not found" >&2
	exit 1
fi

utils=${PWD}/docker/awscli/utils
cfgdir=${PWD}/secret/aws.config

tmpdir=${PWD}/tmp/awscli
install -v -d -m 0750 ${tmpdir}

exec docker run -it --rm --name uws-awscli-env-${envname}-devel \
	--hostname awscli-env-${envname}-devel.uws.local \
	-u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${cfgdir}:/home/uws/config:ro \
	-v ${utils}:/home/uws/bin:ro \
	-v ${tmpdir}:/home/uws/tmp \
	uws/awscli-2211 -il
