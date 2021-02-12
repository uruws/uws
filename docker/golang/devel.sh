#!/bin/sh
exec docker run -it --rm --name uws-golang-devel \
	--hostname golang-devel.uws.local -u uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-v ${PWD}/src/uws:/go/src/uws \
	uws/golang
