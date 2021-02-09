#!/bin/sh
set -eu
mkdir -vp ~/.uws/aws
docker run --rm --name uws-awscli-cmd --hostname awscli-cmd.uws.local -u uws \
	-v ~/.uws/aws:/home/uws/.aws \
	uws/awscli $@
exit 0
