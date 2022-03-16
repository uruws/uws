#!/bin/sh
set -eu
mkdir -vp ~/.aws
docker run --rm --name uws-awscli-cmd --hostname awscli-cmd.uws.local -u uws \
	-v ~/.aws:/home/uws/.aws \
	uws/awscli-2203 "$@"
exit 0
