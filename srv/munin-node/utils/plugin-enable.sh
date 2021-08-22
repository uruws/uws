#!/bin/sh
set -eu

NAME=${1:?'plugin name?'}

PLDIR=/usr/share/munin/plugins
DEST='INVALID'

if test 'Xcontrib' = "X${NAME}"; then
	NAME=${2:?'plugin name?'}
	DEST=${3:-"${NAME}"}
	PLDIR=/uws/munin/contrib/plugins
	plfn=${PLDIR}/${NAME}
	chmod 0755 ${plfn}
elif test 'Xlocal' = "X${NAME}"; then
	NAME=${2:?'plugin name?'}
	DEST=${3:-"${NAME}"}
	PLDIR=/usr/local/bin
elif test 'Xuws' = "X${NAME}"; then
	NAME=${2:?'plugin name?'}
	DEST=${3:-"${NAME}"}
	PLDIR=/uws/bin
else
	DEST=${2:-"${NAME}"}
fi

plfn=${PLDIR}/${NAME}
dstfn=/etc/munin/plugins/${DEST}

rm -f ${dstfn}
ln -vsf ${plfn} ${dstfn}

exit 0
