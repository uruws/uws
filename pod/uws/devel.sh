#!/bin/sh
set -eu
TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}
exec docker run -it --rm --name uws-ca-devel \
	--hostname ca-devel.uws.local -u uws \
	-v ${TMPDIR}:/go/tmp:ro \
	-v ${PWD}/go:/go/src/uws:ro \
	-p 127.0.0.1:2800:2800 \
	--workdir /go/src/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	uws/k8s
