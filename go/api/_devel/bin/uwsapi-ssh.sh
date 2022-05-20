#!/bin/sh
set -eu

cmd=${1:?'cmd?'}

if test 'Xfalse' = "X${cmd}"; then
	exit 1
fi

exit 0
