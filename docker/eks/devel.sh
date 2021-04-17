#!/bin/sh
set -eu
#HEROKU_API_KEY=${HEROKU_API_KEY:-''}
awsdir=${HOME}/.uws/eks/aws
kubedir=${HOME}/.uws/eks/kube
mkdir -vp ${awsdir} ${kubedir}
exec docker run -it --rm --name uws-eks-devel \
	--hostname eks-devel.uws.local -u uws \
	-v ${awsdir}:/home/uws/.aws:ro \
	-v ${kubedir}:/home/uws/.kube \
	uws/eks $@
