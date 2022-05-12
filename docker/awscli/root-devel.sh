#!/bin/sh
set -eu
root=${1:?'root user?'}
awsdir=${PWD}/secret/aws.root/${root}
utils=${PWD}/docker/awscli/utils
if ! test -d ${awsdir}; then
	echo "${awsdir}: root env not found" >&2
	exit 1
fi
exec docker run -it --rm --name uws-awscli-root-${root} \
	--hostname awscli-root-${root}.uws.local \
	-u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${utils}:/home/uws/bin:ro \
	uws/awscli-2203 -il
