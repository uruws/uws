#!/bin/sh
set -eu
dstdir=${1:?'dest dir?'}

install -v -d "${dstdir}/secret/ca/godaddyCerts"
rsync -vax --delete-before \
	${PWD}/secret/ca/godaddyCerts/bundled_all.crt \
	${PWD}/secret/ca/godaddyCerts/server.key \
	"${dstdir}/secret/ca/godaddyCerts/"

exit 0
