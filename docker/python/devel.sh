#!/bin/sh
set -eu
TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}
exec docker run -it --rm --name uws-python-devel \
	--hostname python-devel.uws.local -u uws \
	--read-only \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/python:/opt/uws:ro \
	uws/python-2211
