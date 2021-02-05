#!/bin/sh
set -eu
ENV=${1:-''}
if test "X${ENV}" = 'X'; then
	ENV='dev'
else
	shift
fi
. ./env/${ENV}.env
make $@
exit $?
