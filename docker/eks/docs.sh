#!/bin/sh
set -eu
exec docker run -it --rm --name uws-eks-docs \
	--hostname eks-docs.uws.local -u uws \
	uws/eks-2305 "$@"
