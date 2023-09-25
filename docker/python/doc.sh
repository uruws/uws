#!/bin/sh
set -eu
exec docker run -it --rm --name uws-pydoc \
	--hostname pydoc.uws.local -u uws \
	-p 127.0.0.1:6080:6080 \
	-v ${PWD}/python:/opt/uws \
	-e PYTHONPATH=/opt/uws/lib \
	--entrypoint /usr/bin/pydoc3 \
	uws/python-2309 "$@"
