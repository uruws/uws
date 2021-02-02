#!/bin/sh
set -eu
mkdir -vp ~/.aws
docker run -it --rm --name uws-awscli --hostname awscli.uws.local -u uws \
	-v ~/.aws:/home/uws/.aws \
	uws/awscli $@
exit 0
