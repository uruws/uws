#!/bin/sh
set -eu

awsdir=${PWD}/secret/aws
cfgdir=${PWD}/secret/aws.config
utils=${PWD}/docker/awscli/utils

tmpdir=${PWD}/tmp/awscli
install -v -d -m 0750 ${tmpdir}

exec docker run -it --rm --name uws-awscli-devel \
	--hostname awscli-devel.uws.local \
	-u uws \
	--entrypoint /bin/bash \
	--workdir /home/uws \
	--env-file ${awsdir}/cli.env \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${cfgdir}:/home/uws/config:ro \
	-v ${utils}:/home/uws/bin:ro \
	-v ${tmpdir}:/home/uws/tmp \
	uws/awscli-2309 -il
