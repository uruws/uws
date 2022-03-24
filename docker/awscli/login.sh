#!/bin/sh
set -eu
awsdir=${PWD}/secret/aws
utils=${PWD}/docker/awscli/utils
docker run -it --rm --name uws-awscli-login \
	--hostname awscli-login.uws.local \
	-u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${utils}:/home/uws/bin:ro \
	uws/awscli-2203 -il
exit 0
