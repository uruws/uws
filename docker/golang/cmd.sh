#!/bin/sh
exec docker run --rm --name uws-golang-cmd \
	--hostname golang-cmd.uws.local -u uws \
	-v ${PWD}/src/uws:/go/src/uws \
	uws/golang $@
