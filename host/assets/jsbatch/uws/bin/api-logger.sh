#!/bin/sh
set -eu
container=${1:?'app container?'}
env=${2:?'app env?'}
stdir=${3:-"${HOME}/uws/api/stats"}
export UWS_LOG=quiet
mkdir -p "${stdir}/${env}"
exec docker logs -t --since 4m "${container}" | grep -F ': PARSER_' | sort -k1,1 -u |
	api-logs -env "${env}" -statedir "${stdir}" -statsdir "${stdir}" -kind docker -filter -
