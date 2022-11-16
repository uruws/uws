#!/bin/sh
set -eu
root=${1:?'root user?'}

awsdir=${PWD}/secret/aws.root/${root}
if ! test -d ${awsdir}; then
	echo "${awsdir}: root env not found" >&2
	exit 1
fi

utils=${PWD}/docker/awscli/utils
cfgdir=${PWD}/secret/aws.config

tmpdir=${PWD}/tmp/awscli
install -v -d -m 0750 ${tmpdir}

exec docker run -it --rm --name uws-awscli-root-${root} \
	--hostname awscli-root-${root}.uws.local \
	-u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${cfgdir}:/home/uws/config:ro \
	-v ${utils}:/home/uws/bin:ro \
	-v ${tmpdir}:/home/uws/tmp \
	uws/awscli-2211 -il
