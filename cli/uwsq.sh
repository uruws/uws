#!/bin/sh
set -eu
export NQDIR=/run/uwscli/nq
install -d -m 0750 ${NQDIR}
cd ${NQDIR}
exec fq "$@"
