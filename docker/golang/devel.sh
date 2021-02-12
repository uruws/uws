#!/bin/sh
exec docker run -it --rm --name uws-golang-devel \
	--hostname golang-devel.uws.local -u uws \
	--entrypoint /bin/bash \
	-v ${PWD}:/uws \
	uws/golang
