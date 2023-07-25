#!/bin/sh
set -eu

if test 'X--exec' = "X${1:-X}"; then
	echo "*** devel exec webapp: ${UWS_WEBAPP}"
	cd "/opt/uws/${UWS_WEBAPP}"
	exec "/opt/uws/${UWS_WEBAPP}/run.sh"
fi

echo "*** devel login webapp: ${UWS_WEBAPP}"
exec /bin/bash -il
