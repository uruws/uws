#!/bin/sh
set -eu
mkdir -vp ~/.uws/aws
docker run -it --rm --name uws-awscli --hostname awscli.uws.local -u uws \
	-v ~/.uws/aws:/home/uws/.aws \
	uws/awscli $@
exit 0
