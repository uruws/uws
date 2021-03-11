#!/bin/sh
set -eu
exec docker run -it --rm --name uws-clamav-devel \
	--hostname clamav-devel.uws.local \
	-v ${PWD}:/home/uws/clamav \
	-u uws uws/clamav $@
