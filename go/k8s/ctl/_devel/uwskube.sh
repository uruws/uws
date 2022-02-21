#!/bin/sh
set -eu

if test "X${1}" = 'Xtesting'; then
	exit 0
fi

exit 128
