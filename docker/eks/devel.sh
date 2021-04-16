#!/bin/sh
set -eu
#HEROKU_API_KEY=${HEROKU_API_KEY:-''}
#userdir=${HOME}/uws/heroku
#mkdir -vp ${userdir}
exec docker run -it --rm --name uws-eks-devel \
	--hostname eks-devel.uws.local -u uws \
	uws/eks $@
