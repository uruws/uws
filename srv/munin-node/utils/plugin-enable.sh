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

plfn=${PLDIR}/${NAME}
chmod 0755 ${plfn}

dstfn=/etc/munin/plugins/${DEST}
rm -f ${dstfn}

ln -vsf ${plfn} ${dstfn}
exit 0
