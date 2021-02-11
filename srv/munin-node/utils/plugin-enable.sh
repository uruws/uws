#!/bin/sh
set -eu

NAME=${1:?'plugin name?'}

CONTRIB='false'
PLDIR=/usr/share/munin/plugins
DEST='INVALID'

if test 'Xcontrib' = "X${NAME}"; then
	NAME=${2:?'plugin name?'}
	DEST=${3:?'dest name?'}
	CONTRIB='true'
	PLDIR=/uws/munin/contrib/plugins
else
	DEST=${2:?'dest name?'}
fi

dstfn=/etc/munin/plugins/${DEST}
rm -vf ${dstfn}
ln -vsf ${PLDIR}/${NAME} ${dstfn}

exit 0
