#!/bin/sh
set -eu
MYPYPATH=/uws/lib/plugins
export MYPYPATH
exec python3 -m mypy ${HOME}/k8s/mon/munin-node/plugins \
	${HOME}/k8s/test/mon/munin-node/plugins \
	${HOME}/pod/lib \
	${HOME}/k8s/test/pod/lib
