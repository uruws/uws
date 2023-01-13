#!/bin/sh
set -u

TMPDIR=/srv/acme/run/tmp
mkdir -vp ${TMPDIR}

if test -s ${TMPDIR}/reload; then
	if test 'Xtrue' = "X$(cat ${TMPDIR}/reload)"; then
		nginx -t
		service nginx reload
		echo 'false' >${TMPDIR}/reload
	fi
fi

exit 0
